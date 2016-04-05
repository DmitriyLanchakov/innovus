# -*- coding: utf-8 -*-
import string
from django.template import Node, Variable, Library, TemplateSyntaxError, loader
from django.utils.translation import ugettext as _
from haystack.query import SearchQuerySet
from indexer.utils import LINEAR, LOGARITHMIC, calculate_cloud
from indexer.views import generic_search

register = Library()

@register.tag
def focused(parser, token):
    bits = token.split_contents()
    if len(bits) != 3 or bits[0] != "focused" or bits[1] != "for":
        raise TemplateSyntaxError(
            'Wrong syntax for %(tag)s. Valid is {% %(tag)s ' +
            'for [object] %}' % dict(tag=bits[0])
        )
    return FocusedContentNode(model=bits[2])


class FocusedContentNode(Node):

    def __init__(self, model):
        self.model = Variable(model)

    def render(self, context):
        model = self.model.resolve(context)
        model_ct = ".".join([model._meta.app_label, model._meta.module_name])
        similar_type = point_to_underscore(model_ct)
        language = context['LANGUAGE_CODE']
        tags = [tag.strip() for tag in model.tags.split(',')]
        sqs = SearchQuerySet().filter(tags__in=tags).exclude(django_id = model.pk)
        response = generic_search(language, sqs, similar_type, exclude_text=True)
        response.update({'model_ct': model_ct, 'model_id': model.id, 'selected': None})
        return loader.render_to_string(template_name='indexer/ct_selector.html',
            dictionary=response, context_instance=context)


@register.filter
def humanize_ct(ct):
    HUMANIZED_CT = {
          'periodics.post':  _('News & Events'),
          'library.person':  _('Interviews'),
          'library.picture': _('Images'),
          'library.audio':   _('Audio'),
          'library.video':   _('Video'),
          'library.document':_('Documents'),
          'text.text':       _('Pages'),
    }
    return HUMANIZED_CT.get(ct, ct)

@register.filter
def point_to_underscore(ct):
    return string.replace(ct, '.', '_')


class ThroughTagCloudNode(Node):
    def __init__(self, context_var, **kwargs):
        self.context_var = context_var
        self.kwargs = kwargs

    def render(self, context):
        context[self.context_var] = calculate_cloud(
            context['request'],
            **self.kwargs
        )
        return ''

# --------------------------------------------------------------------------- #

@register.tag
def through_tag_cloud(parser, token):
    """
    Retrieves a list of ``Tag`` objects for  all models, with tag
    cloud attributes set, and stores them in a context variable.

    Usage::

       {% through_tag_cloud as [varname] %}

    Extended usage::

       {% throught_tag_cloud as [varname] with [options] %}

    Extra options can be provided after an optional ``with`` argument,
    with each option being specified in ``[name]=[value]`` format. Valid
    extra options are:

       ``steps``
          Integer. Defines the range of font sizes.

       ``min_count``
          Integer. Defines the minimum number of times a tag must have
          been used to appear in the cloud.

       ``distribution``
          One of ``linear`` or ``log``. Defines the font-size
          distribution algorithm to use when generating the tag cloud.

    Examples::

       {% throught_tag_cloud as widget_tags %}
       {% throught_tag_cloud as widget_tags with steps=9 min_count=3 distribution=log %}

    """
    bits = token.contents.split()
    len_bits = len(bits)
    if len_bits != 3 and len_bits not in range(5, 8):
        raise TemplateSyntaxError(_('%s tag requires either two or between four and six arguments') % bits[0])

    if bits[1] != 'as':
        raise TemplateSyntaxError(_("first argument to %s tag must be 'as'") % bits[0])

    kwargs = {}
    if len_bits > 4:
        if bits[3] != 'with':
            raise TemplateSyntaxError(_("if given, third argument to %s tag must be 'with'") % bits[0])
        for i in range(4, len_bits):
            try:
                name, value = bits[i].split('=')
                if name == 'steps' or name == 'min_count':
                    try:
                        kwargs[str(name)] = int(value)
                    except ValueError:
                        raise TemplateSyntaxError(_("%(tag)s tag's '%(option)s' option was not a valid integer: '%(value)s'") % {
                            'tag': bits[0],
                            'option': name,
                            'value': value,
                        })
                elif name == 'distribution':
                    if value in ['linear', 'log']:
                        kwargs[str(name)] = {'linear': LINEAR, 'log': LOGARITHMIC}[value]
                    else:
                        raise TemplateSyntaxError(_("%(tag)s tag's '%(option)s' option was not a valid choice: '%(value)s'") % {
                            'tag': bits[0],
                            'option': name,
                            'value': value,
                        })
                else:
                    raise TemplateSyntaxError(_("%(tag)s tag was given an invalid option: '%(option)s'") % {
                        'tag': bits[0],
                        'option': name,
                    })
            except ValueError:
                raise TemplateSyntaxError(_("%(tag)s tag was given a badly formatted option: '%(option)s'") % {
                    'tag': bits[0],
                    'option': bits[i],
                })

    return ThroughTagCloudNode(context_var=bits[2], **kwargs)

