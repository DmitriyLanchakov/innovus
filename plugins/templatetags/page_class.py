# -*- coding: utf-8 -*-

from cms.utils import get_language_from_request, get_page_from_request
from cms.utils.moderator import get_cmsplugin_queryset, get_page_queryset
from cms.models import Page
from django import template
from django.contrib.sites.models import Site




register = template.Library()



def send_missing_mail(reverse_id, request):
    site = Site.objects.get_current()
    mail_managers(_('Reverse ID not found on %(domain)s') % {'domain':site.domain},
                   _("A page_id_url template tag didn't found a page with the reverse_id %(reverse_id)s\n"
                     "The url of the page was: http://%(host)s%(path)s")
                     % {'reverse_id':reverse_id, 'host':site.domain, 'path':request.path},
                   fail_silently=True)


class PageAttributeNode(template.Node):
    """This template node is used to output attribute from a page such
    as its title or slug.

    Synopsis
         {% page_attribute field-name %}
         {% page_attribute field-name reverse-id %}

    Example
         {# Output current page's page_title attribute #}
         {% page_attribute page_title %}
         {# Output page_title attribute of the page with reverse_id 'the_page' #}
         {% page_attribute page_title 'the_page' %}


    Keyword arguments:
    field-name -- the name of the field to output. Use one of:
    - title
    - menu_title
    - page_title
    - slug
    - meta_description
    - meta_keywords

    reverse-id -- The page's reverse_id property, if omitted field-name of
    current page is returned.
    """
    def __init__(self, reverse_id=None):
        self.reverse_id = reverse_id


    def render(self, context):
        if not 'request' in context:
            return ''
        lang = get_language_from_request(context['request'])
        page = self._get_page(context['request'])
        if page == "dummy":
            return ''
        if page:
            f = getattr(page, "get_slug")
            return f(language=lang, fallback=True).split('-')[0]
        return ''

    def _get_page(self, request):
        if self.reverse_id == None:
            return request.current_page
        site = Site.objects.get_current()
        try:
            return get_page_queryset(request).get(reverse_id=self.reverse_id, site=site)
        except:
            send_missing_mail(self.reverse_id, request)


def do_page_attribute(parser, token):
    error_string = '%r tag requires one argument' % token.contents[0]
    try:
        # split_contents() knows not to split quoted strings.
        bits = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(error_string)
    if len(bits) >= 1:
        # tag_name, name
        # tag_name, name, reverse_id
        reverse_id = len(bits) == 2 and bits[1] or None
        return PageAttributeNode(reverse_id)
    else:
        raise template.TemplateSyntaxError(error_string)

register.tag('page_slug_class', do_page_attribute)

@register.inclusion_tag('page_title.html', takes_context=True)
def get_title_by_pk(context, page_pk):
    lang = get_language_from_request(context['request'])
    page_title = Page.objects.get(pk = page_pk).get_page_title(language=lang, fallback=True)
    return {
        'title': page_title,
    }

