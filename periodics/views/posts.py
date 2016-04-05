# -*- coding: utf-8 -*-

from calendar import month_name
from cms.utils import get_language_from_request, get_page_from_request
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from annoying.decorators import render_to, ajax_request
from openteam.utils import typograf

from periodics.forms import get_form
from periodics.models import Comment, Post


def get_category_from_request(request, use_session=True):
    """Get category for post at current cms page
    """
    try:
        # key = 'referer' if 'referer' in request.session else 'page_path'
        key = 'page_path'

        if use_session:
            request.path = request.session[key]
        page = get_page_from_request(request)

    except KeyError:
            raise Http404(_('You are behind django-cms'))

    language = get_language_from_request(request)
    cms_category_plugins = page.cmsplugin_set.filter(
        Q(language=language) &
        Q(plugin_type__exact='PageCategoryPlugin')
    )

    if cms_category_plugins.count() != 1:
        raise Http404(_('Category not found'))

    return cms_category_plugins[0].pagecategory.category


def get_form_errors(form):
    """
    Returns dictionary of fields and its validation errors (in HTML)
    """
    errors = {}
    for k in form.errors:
        errors[k] = unicode(form.errors[k])
    return errors

# --------------------------------------------------------------------------- #

@ajax_request
def add_comment(request, parent_id=None):
    result = dict(errors={},success=False)
    request.META.update(parent_id=parent_id)

    ## Если указан parent_id, то информацию о комментируемом объекте
    ## получаем из контент-объекта родительского комментария
    if parent_id:
        comment_parent = get_object_or_404(Comment, pk=parent_id)
        commentable    = comment_parent.commentable

    ## Или получить его из формы
    ##
    else:
        post_id = request.POST.get('post')
        ctype   = request.POST.get('type')
        comment_parent = None

        app_label, model = ctype.split('_')

        commentable = get_object_or_404(
            get_object_or_404(ContentType, model=model, app_label=app_label).model_class(),
            pk = post_id,
        )

    ## TODO этот кусок дублируется в comments_tags. Убрать дублирование
    form_class = get_form(request)
    form = form_class(request.POST)

#    if isinstance(commentable, Post):
#        comments_allow, premoderate = object_comments_settings(
#            category = get_category_from_request(request, True),
#            post     = commentable
#        )
#
#    else:
#        comments_allow, premoderate = True, False
    comments_allow, premoderate = True, False

    if form.is_valid():
        instance = Comment(
            content = typograf(form.cleaned_data['content']),
            ip_address  = request.META.get('REMOTE_ADDR'),
            commentable = commentable,
            is_approved = not premoderate,
            )

        if request.user.is_authenticated():
            instance.user = request.user

        else:
            instance.author_name  = form.cleaned_data['author_name']
            instance.author_email = form.cleaned_data['author_email']

        # Makes reply if parent comment specified
        if comment_parent:
            instance.insert_at(
                comment_parent,
                position = 'last-child',
                commit   = False
            )

        instance.save()

        result.update({
            'success': True,
            'parent': comment_parent.id if comment_parent else None,
            'comment': render_to_string('periodics/comments/item.html',
                        {'comment': instance,})
        })
    else:
        result['errors'] = get_form_errors(form)

    # ----------------------------------------------------------------------- #
    # Form is filled correctly
    if result['success']:
        if premoderate:
            result['comment'] = render_to_string(
                'periodics/comments/show_later.html',
                dict(comment=instance),
                RequestContext(request)
            );

        return result
    # There are some validation errors
    else:
        return result


def show(request, pk, slug):

    try:
        request.session['page_path'] = request.path
        category = get_category_from_request(request)
        post = category.posts.actual().get(pk=pk, slug=slug)

    except Post.DoesNotExist:
        raise Http404(_('God damn!'))
    #TODO: write normal tokenizer
    tags = [ tag.strip(' ') for tag in post.tags.split(',') ]
    tags = [ tag for tag in tags if len(tag) ]

#    debug(tags)

    return render_to_response(
        category.post_template,
        {
            'post': post,
            'category': category,
            'templates': dict(
                video = 'periodics/content/video_large.html',
                image = 'periodics/content/image_large.html',
                error = 'periodics/content/error.html',
            ),
            'tags':  tags,
            'view_title': post.title,
        },
        RequestContext(request)
    )

# --------------------------------------------------------------------------- #

@render_to('periodics/archive_dates.html')
def archive(request):
    page = get_page_from_request(request)
    language = get_language_from_request(request)
    category = get_category_from_parent(page, language)


    archive = []
    posts = category.posts.actual()
    years = posts.dates('public_from','year', order='DESC')

    for year in years:

        months = posts.filter(public_from__year = year.year).dates('public_from','month', order='ASC')
        archive.append([year.year, [ (date.month, _(month_name[date.month]) ) for date in months ]])

    return { 'archive': archive, 'category': category, 'current_page': get_page_from_request(request) }

# --------------------------------------------------------------------------- #

@render_to('periodics/archive_posts.html')
def by_date(request, year=None, month=None):
    page = get_page_from_request(request)
    language = get_language_from_request(request)
    category = get_category_from_parent(page, language)

    posts = category.posts.actual()

    if year and not month:
        posts = posts.filter(public_from__year = year)
    elif year and month:
        posts = posts.filter( Q(public_from__year = year) & Q(public_from__month = month) )

    return { 'category': category, 'posts': posts }

# --------------------------------------------------------------------------- #

def get_category_from_parent(page, language):
    cms_category_plugins = page.parent.cmsplugin_set.filter(
          Q(language=language) &
          Q(plugin_type__exact='PageCategoryPlugin')
     )
    return cms_category_plugins[0].pagecategory.category

