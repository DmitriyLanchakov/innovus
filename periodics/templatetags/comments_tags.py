# -*- coding: utf-8 -*-

from django import template
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from annoying.functions import get_object_or_None
from openteam.utils import html2text

from periodics.models import Comment, BannedIp
from periodics.forms  import get_form

# --------------------------------------------------------------------------- #

register = template.Library()

# --------------------------------------------------------------------------- #

def object_comments_settings(post, category):
    DEFAULT_ALLOW = True
    DEFAULT_PREMODERATE = False

    # Reset settings
    allow, premoderate = False, False

    #
    if post.publisher_public:
        post = post.publisher_public

    # Checks for comments for post in category are allowed
    if post.comments_allow is not None:
        allow = post.comments_allow
    else:
        allow = category.is_commented if category else DEFAULT_ALLOW

    # If comments is allowed, checks for premoderation
    if allow:
        if post.comments_premoderate is not None:
            premoderate = post.comments_premoderate
        else:
            premoderate = category.is_moderated if category else DEFAULT_PREMODERATE

    #
    return allow, premoderate

# --------------------------------------------------------------------------- #

class CommentsBaseNode(template.Node):
    def __init__(self, post, category):
        self.post = template.Variable(post)
        self.category = template.Variable(category)

# --------------------------------------------------------------------------- #

class CommentsMainNode(CommentsBaseNode):

    def render(self, context):
        category = self.category.resolve(context)
        if category and not category.is_commented:
            return ''
        return render_to_string('periodics/comments/main.html', {
                'request'  : context['request'],
                'post'     : self.post.resolve(context),
                'category' : category,},
                context_instance=RequestContext(context['request']))


class CommentsFormNode(CommentsBaseNode):
    def __init__(self, post, category, parent=None):
        self.post = template.Variable(post)
        self.parent = template.Variable(parent) if parent else None
        self.category = template.Variable(category)

    def render(self, context):
        post     = self.post.resolve(context)
        category = self.category.resolve(context)
        parent   = self.parent.resolve(context) if self.parent else None
        request  = context['request']

        if request.method == 'GET':
            request.session['page_path'] = request.path

        # Define the form class
        form_class = get_form(request)


        if request.method == 'POST':
            comment_form  = form_class(request.POST, initial={'post': post.pk})
            comment_form.is_valid()

        else:
            ct = ContentType.objects.get_for_model(post)
            comment_form = form_class(
                initial = dict(
                    post = post.pk,
                    type = "_".join([ct.app_label, ct.model]),
                )
            )
        comments_allow, comments_premoderate = object_comments_settings(post, category)
        ip_banned = get_object_or_None(BannedIp, ip_address=request.META.get('REMOTE_ADDR'))

        return render_to_string('periodics/comments/form.html', dict(
            request  = request,
            post     = post,
            category = category,
            parent   = parent,
            comment_form     = comment_form,
            premoderate      = comments_premoderate,
            ip_banned        = ip_banned,
            comments_allow   = comments_allow,
            ), context_instance = RequestContext(request)
        )

# --------------------------------------------------------------------------- #

class CommentsListNode(template.Node):
    def __init__(self, object, varname, category=None):
        self.object   = template.Variable(object)
        self.category = template.Variable(category) if category else None
        self.varname  = varname

    def render(self, context):
        # Workaround comments count for not created posts (in admin area, e.g.)
        try:
           object   = self.object.resolve(context)
        except:
            return ''

        category = self.category.resolve(context) if self.category else None

        if not object:
            return ''

        # Gets comment settings for post in category

        comments_allow, comments_premoderate = object_comments_settings(object, category)

        if comments_allow:
            queryset = Comment.objects.select_related('_commentable_content_type')

            if comments_premoderate:
                pass # we needn't is_approved filter for premoderated!

            # Changes context dictionary
            context[self.varname] = queryset.filter(
                _commentable_content_type = ContentType.objects.get_for_model(object),
                _commentable_object_id    = object.id
            ).order_by('tree_id', 'lft', 'created_at')

            return unicode('')


class CommentsCountNode(CommentsListNode):
    def render(self, context):
        super(CommentsCountNode, self).render(context)

        if context.has_key(self.varname):
            context[self.varname] = context[self.varname].approved().count()
        return ''


class CommentsFormActionNode(template.Node):
    def __init__(self, parent=None):
        self.parent = template.Variable(parent) if parent else None

    def render(self, context):
        parent = self.parent.resolve(context) if self.parent else None

        if parent:
            return reverse('comment-reply', kwargs={'parent_id': parent.id,})
        else:
            return reverse('comment-add')

# --------------------------------------------------------------------------- #

class CommentsLastNode(template.Node):
    def __init__(self, queryset, varname):
        self.queryset = template.Variable(queryset)
        self.varname = template.Variable(varname)

    def render(self, context):
        queryset = self.queryset.resolve(context)
        varname  = self.varname.resolve(context)

        context[varname] = queryset.filter(level=0).order_by('-created_at')[:3]
        return ''

# --------------------------------------------------------------------------- #

@register.tag
def admin_get_comments_list(parser, token):
    bits = token.split_contents()
    object, varname = None, None
    if len(bits) < 5 or bits[1] != 'for' or bits[3] != 'as':
        raise template.TemplateSyntaxError(
            'Format: {% admin_get_comments_list for [object] as [var] %}'
        )

    object   = bits[2]
    varname  = bits[4]

    return CommentsListNode(
        object   = object,
        varname  = varname,
        category = None,
    )

# --------------------------------------------------------------------------- #

@register.tag
def get_comments_list(parser, token):
    bits = token.split_contents()

    if len(bits) < 7 or bits[1] != 'for' or bits[3] != 'in' or bits[5] != 'as':
        raise template.TemplateSyntaxError(
            'Format: {% get_comments_list for [object] in [category] as [var] %}'
        )

    object   = bits[2]
    category = bits[4]
    varname  = bits[6]

    return CommentsListNode(
        object   = object,
        varname  = varname,
        category = category,
)

# --------------------------------------------------------------------------- #

@register.tag
def get_comments_count(parser, token):
    bits = token.split_contents()

    if len(bits) < 7 or bits[1] != 'for' or bits[3] != 'in' or bits[5] != 'as':
        raise template.TemplateSyntaxError(
            'Format: {% get_comments_count for [object] in [category] as [var] %}'
        )

    object   = bits[2]
    category = bits[4]
    varname  = bits[6]

    return CommentsCountNode(
        object   = object,
        varname  = varname,
        category = category,
    )

# --------------------------------------------------------------------------- #

@register.tag
def comments_form(parser, token):
    post, category, parent = None, None, None
    bits = token.split_contents()

    if len(bits) < 5 or bits[1] != 'for' or bits[3] != 'in':
        raise template.TemplateSyntaxError(
            'Format: {% comments_form for [object] in [category] %} ' + \
            'or {% comments_form for [object] in [category] reply_to=[parent] %}'
        )

    if len(bits) == 6 and bits[5].startswith('reply_to'):
        trash, parent = bits[5].split('=', 2)

    return CommentsFormNode(
        post     = bits[2],
        category = bits[4],
        parent   = parent,
    )

# --------------------------------------------------------------------------- #

@register.tag
def comments(parser, token):
    bits = token.split_contents()

    if len(bits) != 5 or bits[1] != 'for' or bits[3] != 'in':
        raise template.TemplateSyntaxError(
            'Format: {% comments for [object] in [category] %}'
        )

    return CommentsMainNode(
        post     = bits[2],
        category = bits[4],
    )

# --------------------------------------------------------------------------- #

@register.tag
def comments_form_action(parser, token):
    bits, parent = token.split_contents(), None
    if len(bits) > 1:
        parent = bits[1]

    return CommentsFormActionNode(parent=parent)

# --------------------------------------------------------------------------- #

@register.tag
def comments_last(parser, token):
    bits = token.split_contents()

    if len(bits) != 4 and bits[2] != 'as':
        raise template.TemplateSyntaxError(
            'Format: {% comments_last [queryset] as [varname] %}'
        )

    queryset = bits[1]
    varname  = bits[3]

    return CommentsLastNode(queryset, varname)

# --------------------------------------------------------------------------- #

register.filter(html2text)

