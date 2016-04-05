# -*- coding: utf-8 -*-
from cms.utils import get_language_from_request
from django.contrib.auth.views import *
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template import loader
from django.template.context import RequestContext
from django.core.paginator import Paginator
from annoying.decorators import ajax_request, render_to
from ajax.utils import get_int_safe
from periodics.models import Post, Category
from plugins.models import Toggle


def get_slice_offsets(page, size):
    """
    Gets absolute slice offset markers
    """
    page = page if page > 0 else 1
    return size * (page - 1), size * page

def get_objects_and_last_flag(queryset, page, size):
    """
    Retrieves actual slice of queryset and check is there more entries
    """
    paginator = Paginator(queryset, size)
    page = paginator.page(page)
    return page.object_list, not page.has_next()

@ajax_request
def last_news(request, sequence):
    size = 3
    page = abs(get_int_safe(request, 'page', 1))
    # Retrieve page post set
    language = get_language_from_request(request)
    categories = Category.objects.filter(pk__in = settings.NEWS_AGREGATE_CATEGORIES[language][sequence])
    posts, is_last = get_objects_and_last_flag(
        queryset = Post.objects.public().filter(category__in=categories).order_by('-public_from'),
        page     = page,
        size     = size
    )
    # Retrieve a oldest post
    templates = {
        'inno' : 'plugins/inno_news_ul.html',
        'site' : 'plugins/fresh_ul.html'
    }
    return {'last': is_last,
            'text': loader.render_to_string(templates[sequence],
                {'posts': posts, 'is_last': is_last},
                RequestContext(request))}


#@ajax_request
#def persons_list(request):
#    page = abs(get_int_safe(request, 'page', 1))
#    plugin  = get_object_or_404(Persons, pk=request.GET.get('plugin'))
#    categories = plugin.categories.all()
#    size = plugin.per_page
#    persons, is_last = get_objects_and_last_flag(
#        queryset = Person.objects.public().filter(category__in = categories).order_by('sort_order'),
#        page = page,
#        size = size
#    )
#
#    return {'persons':
#                loader.render_to_string('plugins/persons/ul.html', {
#                    'object': plugin,
#                    'persons': persons},
#                    context_instance=RequestContext(request)),
#            'links':
#                loader.render_to_string('plugins/persons/nav.html', {
#                    'is_first': page == 1,
#                    'is_last': is_last,
#                    'object': plugin,},
#                    context_instance=RequestContext(request)),
#            }


@ajax_request
def events(request):
    language = get_language_from_request(request)
    post = get_object_or_404(Post,
        pk = get_int_safe(request, 'event'),
        category__in = settings.NEWS_AGREGATE_CATEGORIES[language]['events']
    )
    return {'media': loader.render_to_string('plugins/events_inline_media.html',
                {'post': post},
                context_instance=RequestContext(request)),
            'content': loader.render_to_string('plugins/events_inline_content.html',
                {'post':post},
                context_instance=RequestContext(request)),
            'comments': loader.render_to_string('plugins/events_inline_comments.html',
                {'post': post},
                context_instance=RequestContext(request)),
            }


@ajax_request
def load_hidden_text(request, id):
    language = get_language_from_request(request)
    plugin_model = get_object_or_404(Toggle, pk=id)
    try:
        toggle = plugin_model.page.cmsplugin_set.public().get(
            language=language, plugin_type='TogglePlugin', pk=id)
        return {'html': toggle.render_plugin(context={'is_ajax': True})}
    except:
        raise Http404

@render_to('blank.html')
def render_archive_years(request):
    return {'is_ajax': True}

