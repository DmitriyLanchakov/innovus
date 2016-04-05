# encoding: utf-8
from __future__ import absolute_import
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language_from_request
from profile.models import Claim
from profile import settings as profile_settings
from events.models import ForumEvent, ForumEventContent


@login_required
@render_to('profile/events/list.html')
def index(request, id=None):
    manager = get_object_or_None(Claim, user=request.user)
    if id and manager:
        claim = get_object_or_404(Claim, id=id, delegation_manager=manager)
    elif id and request.user.is_staff:
        claim = get_object_or_404(Claim, id=id)
    else:
        claim = get_object_or_404(Claim, user=request.user, is_take_part__in=[
                profile_settings.TAKE_PART_P,
                profile_settings.TAKE_PART_CONTACT_W_P])
    if request.POST:
        claim.events.clear()
        for event_id in request.POST.getlist('event'):
            event = get_object_or_None(ForumEvent, id=event_id)
            if event:
                claim.events.add(event)
        messages.success(request,_('Events schedule was successfully updated'))
        return redirect(request.path)

    language = get_language_from_request(request)
    events = ForumEvent.objects.filter(forum__is_current=True)
    if claim.programm_type == profile_settings.PROGRAMM_TYPE_YOUTH:
        events = events.filter(can_register_youth=True)
    if claim.programm_type == profile_settings.PROGRAMM_TYPE_GENERAL:
        events = events.filter(can_register_business=True)
    days = events.dates('starts_on', 'day')
    events_set = [[day, events.filter(starts_on__day=day.day)] for day in days ]
    events_content = ForumEventContent.objects.filter(
        language=language, display=True)
    for set in events_set:
        set[1] = events_content.filter(event__in = set[1]).order_by('event__starts_on')

    return {'events': events, 'claim': claim, 'manager': manager, 'events_list': claim.delegates.count(),
            'events_set': events_set}

#@render_to('profile/events/list_print.html')
#def list_events_print(request):
#    events = Event.objects.order_by('date_started', 'sort_order',)
#
#    return dict(
#        events = events,
#    )
#
#
#@ajax_request
#def ajax_event_details(request, event_id):
#    event = get_object_or_404(Event, pk=event_id)
#    lang  = get_language_from_request(request)
#    english = lang == 'en'
#
#    return dict(
#            language    = lang,
#            event_type  = event.get_event_type_display(),
#            title       = getattr(event, 'title_en' if english else 'title'),
#            annotation  = getattr(event, 'annotation_en' if english else 'annotation'),
#            description = getattr(event, 'description_en' if english else 'description'),
#        )
