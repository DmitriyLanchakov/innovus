# -*- coding: utf-8 -*-

from itertools import chain
from django.template import Node, Library, Variable, TemplateSyntaxError
from django.forms import widgets
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from profile.models import *

# --------------------------------------------------------------------------- #

register = Library()

# --------------------------------------------------------------------------- #

@register.tag
def localize_select(parser, token):
    """
    Usage: {% localize_select select %}
    """
    class LocalizedSelect(widgets.Select):
        """
        Custom select widget for options translations
        """
        def __init__(self, language, field, *args, **kwargs):
            self.language = language
            self.field = field

            super(LocalizedSelect, self).__init__(*args, **kwargs)

        def render_options(self, choices, selected_choices):
            def render_option(option_value, option_label):
                option_value = force_unicode(option_value)

                clean_values = [int(i) if str(i).isdigit() else '' for i in selected_choices]
                clean_value = int(option_value) if option_value.isdigit() else ''
                selected_html = (clean_value in clean_values) and \
                    u' selected="selected"' or ''

                return u'<option value="%s"%s>%s</option>' % (
                    escape(option_value), selected_html,
                    conditional_escape(force_unicode(option_label)))

            # Recognize current language

            # Default value
            output = [
                render_option('', '----------')
            ]

            # Queryset values
            for option in self.field.queryset:
                output.append(
                    render_option(
                        option.pk,
                        getattr(option, 'title%s' % ('_en' if self.language == 'en' else ''))
                    )
                )

            return u'\n'.join(output)

    # ----------------------------------------------------------------------- #

    class LocalizeSelectNode(Node):
        """
        LocalizeSelect template node
        """
        def __init__(self, select):
            self.select = Variable(select)

        def render(self, context):
            select = self.select.resolve(context)

            select.field.widget = LocalizedSelect(
                language = context['LANGUAGE_CODE'],
                field    = select.field,
            )

            return unicode(select)

    # ----------------------------------------------------------------------- #

    bits = token.split_contents()

    if len(bits) != 2:
        raise TemplateSyntaxError(
            'Wrong syntax for %s. Use {%% %s select %%}' % (bits[0], bits[0])
        )

    select = bits[1]

    return LocalizeSelectNode(select)

# --------------------------------------------------------------------------- #

@register.tag
def localize_verbose_name(parser, token):
    class LocalizeVerboseNameNode(Node):
        def __init__(self,  field):
            self.field = Variable(field)

        def render(self, context):
            field = self.field.resolve(context)

            for f in Claim._meta.fields:             
                if f.name == field:
                    return f.verbose_name
            return field

    bits = token.split_contents()   
    return LocalizeVerboseNameNode(bits[1])
    
