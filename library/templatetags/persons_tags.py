from math import ceil
from django.template import Node, Library, Variable, TemplateSyntaxError
from django.core.urlresolvers import reverse
from ajax.utils import get_int_safe
from library.models import Person

register = Library()


class LinkNode(Node):
    def __init__(self, object, direction):
        self.object = Variable(object)
        self.direction = direction

    def render(self, context):
        instance = self.object.resolve(context)
        request  = context.get('request')

        # Current requested page
        page = get_int_safe(request, 'page', 1)

        total_pages = ceil(
            float(Person.objects.filter(
                category__in=instance.category.all()
            ).count()) / instance.per_page)

        if (self.direction == 'next' and page >= total_pages) or \
           (self.direction == 'prev' and page == 1):
                return '#'

        return reverse('ajax_persons_list') + \
            '?plugin=%(instance)d&amp;page=%(page)d' % dict(
            instance = instance.pk,
            page     = page + 1 if self.direction == 'next' else page - 1,
        )


def tag_link(parser, token, direction):
    bits = token.split_contents()

    if len(bits) != 3 or bits[1] != 'for':
        raise TemplateSyntaxError(
            'Wrong syntax. Please use {%% %s for [object] %%}' % bits[0]
        )

    return LinkNode(bits[2], direction)


@register.tag
def link_prev(parser, token):
    return tag_link(parser, token, 'prev')


@register.tag
def link_next(parser, token):
    return tag_link(parser, token, 'next')

