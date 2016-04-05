# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin, Title
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from profile.models import *
from profile import settings as profile_settings

from datetime import timedelta
# --------------------------------------------------------------------------- #

class RegistrationPlugin(CMSPluginBase):
    admin_preview = False
    model = CMSPlugin

    name  = _('Registration page')
    render_template = 'plugins/profile/registration.html'

    def render(self, context, instance, placeholder):
        self.render_template = instance.template or self.render_template
        context.update(
            dict(
                object = instance,
            )
        )
        return context

# --------------------------------------------------------------------------- #
TAKE_PART_P = 1
TAKE_PART_CONTACT_WO_P = 2
TAKE_PART_CONTACT_W_P  = 3
TAKE_PART_DELEGATE     = 4

class ParticipantsPlugin(CMSPluginBase):
    admin_preview = False
    model = Participants

    name  = _('Participants page')
    render_template = 'profile/participants.html'

    def render(self, context, instance, placeholder):
        self.render_template = instance.template or self.render_template
        context.update(
            dict(
                object = instance,
                per_page = instance.per_page or 10,
                participants = Claim.objects.filter(
                    is_take_part__in = [
                        TAKE_PART_P,
                        TAKE_PART_CONTACT_W_P,
                        TAKE_PART_DELEGATE
                    ]).filter(
                    claim_state__in = [
                        profile_settings.CLAIM_SENT,
                        profile_settings.CLAIM_WAITING_APPROVEMENT,
                        profile_settings.CLAIM_WAITING_PAYMENT,
                        profile_settings.CLAIM_ACCEPTED,
                    ]).order_by("last_name", "first_name", "middle_name"),
            )
        )
        return context

# --------------------------------------------------------------------------- #
#
#class EventsPlugin(CMSPluginBase):
#    admin_preview = False
#    model = Events
#
#    name  = _('Events page')
#    render_template = 'profile/events.html'
#
#    def render(self, context, instance, placeholder):
#        self.render_template = instance.template or self.render_template
#        context.update(
#            dict(
#                object = instance,
#                events = Event.objects.filter(
#                    date_started__month = instance.date.month,
#                    date_started__year  = instance.date.year,
#                    date_started__day   = instance.date.day,
#                ).order_by('date_started', 'sort_order'),
#            )
#        )
#        return context

# --------------------------------------------------------------------------- #
#
#class BroadcastPlugin(CMSPluginBase):
#    admin_preview = False
#    model = EventsNow
#
#    name  = _('Events broadcast')
#    render_template = 'plugins/broadcast.html'
#
#    def render(self, context, instance, placeholder):
#        self.render_template = instance.template or self.render_template
#        now = datetime.now()
#        delta5min = timedelta(minutes=5)
#
#        context.update(
#            {
#                'object': instance,
#                'events': Event.objects.filter(
#                    date_started__lte = (now + delta5min),
#                    date_finished__gte = (now - delta5min),
#                    is_displayable = True,
#                ).order_by('date_started', 'event_type', 'sort_order'),
#            }
#        )
#        return context


# --------------------------------------------------------------------------- #
#plugin_pool.register_plugin(BroadcastPlugin)
#plugin_pool.register_plugin(EventsPlugin)
plugin_pool.register_plugin(RegistrationPlugin)
plugin_pool.register_plugin(ParticipantsPlugin)

