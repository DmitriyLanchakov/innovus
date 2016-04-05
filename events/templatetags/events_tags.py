from django import template
from django.utils.translation import ugettext_lazy as _
from cms.models import Page
from events.plugins.models import ForumHistory
from events.models import ForumEvent, ForumEventContent


register = template.Library()

@register.tag
def forum_event_attr(parser, token):
    bits = token.split_contents()
    if len(bits) < 4 or bits[2] != "for":
        raise template.TemplateSyntaxError, "forum_event_attribute syntax is: forum_event_attr <attr_name> for <event>"
    if len(bits) == 6 and bits[4] == "as":
        return ForumEventAttributeNode(event=bits[3], attr=bits[1], var=bits[5])
    return ForumEventAttributeNode(event=bits[3], attr=bits[1])

class ForumEventAttributeNode(template.Node):

    def __init__(self, attr, event, var=None):
        self.attr = attr
        self.event = event
        self.var = var

    def render(self, context):
        attr_value = ""
        language = context.get('LANGUAGE_CODE','ru')
        event = template.Variable(self.event).resolve(context)
        if getattr(event, self.attr, None):
            attr_value = getattr(event, self.attr)
        else:
            content = event.event_contents.filter(language=language)
            if content.count() and getattr(content[0], self.attr, None):
                attr_value = getattr(content[0], self.attr)

        if self.var:
            context.update({self.var: attr_value})
            return ""
        return attr_value


@register.tag
def forum_events(parser, token):
    return ForumEventsNode()


class ForumEventsNode(template.Node):

    def __init__(self):
        pass

    def render(self, context):
        page = context['request'].current_page
        plugin = find_forum_plugin(page)
        if plugin and plugin.forum:
            language = context.get('LANGUAGE_CODE', 'ru')
            content_items = ForumEventContent.objects.filter(event__forum=plugin.forum,
                language=language, display=True)
            types_distinct = {}
            for key in ForumEventContent.objects.filter(event__forum=plugin.forum,
                    language=language, display=True).values_list('event__programm_type').distinct():
                if key[0] not in types_distinct:
                    types_distinct.update(dict(
                        filter(lambda x: x[0] == key[0], ForumEvent.PROGRAM_TYPES.get_choices())
                        ))
            return template.loader.render_to_string("events/forum_history.html",
                    {'items': content_items, 
                     'program_types': types_distinct}, 
                    template.RequestContext(context['request']))
        return ""


@register.tag
def forum_attribute(parser, token):
    bits = token.split_contents()
    bitlength = len(bits)
    if bitlength < 2:
        raise template.TemplateSyntaxError, _("forum attribute requires attribute name")
    elif bitlength == 4 and bits[2] == 'as':
        return ForumAttributeNode(attr=bits[1], var=bits[3])
    return ForumAttributeNode(attr=bits[1])


class ForumAttributeNode(template.Node):

    def __init__(self, attr, var=None):
        self.attr = attr
        self.var = var

    def render(self, context):
        page = context['request'].current_page
        plugin = find_forum_plugin(page)
        if plugin and plugin.forum:
            attribute_value = getattr(plugin.forum, self.attr, '')
            if self.var:
                context.update({self.var: attribute_value})
            else:
                return attribute_value
        return ""


def find_forum_plugin(page):
    if isinstance(page, Page):
        plugins = ForumHistory.objects.filter(page=page)
        if plugins.count():
            return plugins[0]
        else:
            if page.parent:
                return find_forum_plugin(page.parent)
    return None
