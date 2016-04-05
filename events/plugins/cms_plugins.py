import os
from datetime import datetime, timedelta
from cms.models import CMSPlugin
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from events.models import ForumEventContent
from events.plugins.models import ForumProgramm, ForumHistory, Broadcast


class ForumProgrammPlugin(CMSPluginBase):
    admin_preview = False
    model = ForumProgramm
    name = _("forum programm")
    render_template = "events/programm.html"

    def render(self, context, instance, placeholder):
        events = instance.forum.events.filter(programm_type=instance.program_type)
        days = events.dates('starts_on', 'day')
        events_set = [[day, events.filter(starts_on__day=day.day)] for day in days ]
        events_content = ForumEventContent.objects.filter(
            language=context['LANGUAGE_CODE'], display=True)
        for set in events_set:
            set[1] = events_content.filter(event__in = set[1]).order_by('event__starts_on')

        context.update({'events_set': events_set,
                        'object': instance,
                        'programm_type': instance.program_type,
                        'placeholder': placeholder,})
        return context


plugin_pool.register_plugin(ForumProgrammPlugin)


class ForumEventOnPage(CMSPluginBase):
    admin_preview = False
    model = CMSPlugin
    name = _("forum event on page")
    render_template = "events/event_on_page.html"

    def render(self, context, instance, placeholder):
        from library.models.persons import PersonToCategory
        now = datetime.now()
        language = context.get('LANGUAGE_CODE', 'ru')
        events = ForumEventContent.objects.filter(language=language).filter(cms_page = instance.page)
        if events.count:
            event = events[0]
            if event.moderators:
                moderators = PersonToCategory.objects.filter(
                    category=event.moderators,
                    related_model__in=event.moderators.persons.all()).order_by('sort_order')
            else:
                moderators = None
            context.update({
                'moderators': moderators,
                'event': event,
                'category': None,
                'object': instance,
                'placeholder': placeholder })
            if (event.event.videostream and event.event.broadcast_start <= now and
                    event.event.broadcast_end >= now):
                context.update({
                    'broadcast': render_to_string(
                        "events/event_broadcast_on_page.html", context)
                })
        return context


plugin_pool.register_plugin(ForumEventOnPage)


class ForumEventOnHistoryPage(ForumEventOnPage):
    render_template = "events/event_on_history_page.html"
    name = _("forum event on history page")


plugin_pool.register_plugin(ForumEventOnHistoryPage)

class ForumEventComments(ForumEventOnPage):
    name = _('comments for event on page')
    render_template = "events/comments_for_event.html"


plugin_pool.register_plugin(ForumEventComments)


class ForumHistoryPlugin(CMSPluginBase):
    admin_preview = False
    model = ForumHistory
    name = _("forum events history")
    render_template = "blank.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder })
        return context

plugin_pool.register_plugin(ForumHistoryPlugin)


class ForumEventBroadcastPlugin(CMSPluginBase):
    admin_preview = False
    model = Broadcast
    render_template = "events/event_broadcast.html"
    name = _("Forum events broadcast")

    def render(self, context, instance, placeholder):
        language = context.get('LANGUAGE_CODE', 'ru')
        five_minutes = timedelta(minutes=5)
        start = datetime.now() + five_minutes
        end = datetime.now() - five_minutes
        # get events base models scheduled for now with 5 min lag
        events = instance.forum.events.filter(broadcast_start__lte=start,
                broadcast_end__gte=end)
        # get events content containers
        contents = ForumEventContent.objects.filter(
                event__in=events, language=language).order_by('event__starts_on')
        streamdict = {'playlist': []}
        context.update({'events': []})
        # fill in playlist dict
        for content in contents:
            if content.event.videostream:
                streamdict['playlist'].append({
                    'file': content.event.videostream,
                    'comment': content.name})
                context['events'].append(content)
        # process information channel broadcasting
        if instance.channel_display:
            same_channel = [ instance.channel_stream for stream in
                    streamdict['playlist'] if stream['file'] ==
                    instance.channel_stream ]
            if len(same_channel) == 0:
                streamdict['playlist'].append({
                    'file': instance.channel_stream,
                    'comment': instance.channel_title,
                    })

        playlist_path = os.path.join(settings.MEDIA_ROOT, 'static', 'css',
            'playlist-broadcast.txt')
        context.update({'show': len(streamdict['playlist'])})
        # dumps playlist as json file, suitable for uppod player
        with open(playlist_path, 'w') as fp:
            fp.write(simplejson.dumps(streamdict))
        return context


plugin_pool.register_plugin(ForumEventBroadcastPlugin)
