from django.contrib.admin.views.main import SEARCH_VAR
from django.template import loader, Library, Node, Variable, TemplateSyntaxError
from library.models import *

register = Library()

@register.tag
def multimedia(parser, token):
    template_map = {
        Video    : 'video',
        Audio    : 'audio',
        Picture  : 'picture',
        Document : 'document',
    }

    class MultimediaNode(Node):
        def __init__(self, resource):
            self.resource = Variable(resource)

        def render(self, context):
            resource = self.resource.resolve(context)
            template = template_map[resource] if resource.__class__ \
                in template_map else 'error'

            return loader.render_to_string(
                'plugins/resources/templatetags/%s.html' % template,
                dict(
                    resource = resource,
                ),
            )
    bits = token.split_contents()

    if len(bits) != 3 or bits[0] != "multimedia" or bits[1] != "for":
        raise TemplateSyntaxError(
            'Wrong syntax for %(tag)s. Valid is {% %(tag)s ' +
            'for [object] %}' % dict(tag=bits[0])
    )

    return MultimediaNode(post=bits[2])

@register.inclusion_tag('admin/library/resource/search_form.html', takes_context=True)
def history_search_form(context):
    """
    Displays a search form for searching the list.
    """
    cl = context['cl']
    context.update({
        'cl': cl,
        'show_result_count': cl.result_count != cl.full_result_count,
        'search_var': SEARCH_VAR,
        'categories': Category.objects.all(),
        'selected_cat': int(context['request'].GET.get('category__id__exact', 0))
    })

    return context

from django.contrib.admin.templatetags.admin_list import result_hidden_fields, result_headers, results

@register.tag 
def library_result_list(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError, "syntax is <library_result_list cl>"

    return ResultListNode(bits[1])

class ResultListNode(Node):

    def __init__(self, cl):
        self.cl = cl

    def render(self, context):
        cl = Variable(self.cl).resolve(context)
        
        cat_id = context['request'].GET.get('category__id__exact')
        if cat_id:
            # positions = cl.model.positions.get(id=cat_id)
            position_model = cl.model.positions.related.model
            positions = position_model.objects.filter(category=cat_id, related_model__in=cl.result_list).order_by('sort_order')
            cl.result_list = [position.related_model for position in positions]

        return loader.render_to_string("admin/change_list_results.html", {
            'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': list(result_headers(cl)),
            'results': list(results(cl))}
            )
# inclusion_tag("admin/change_list_results.html")

