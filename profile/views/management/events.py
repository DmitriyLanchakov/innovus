# encoding: utf-8
from __future__ import absolute_import
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.db.models import Q
from django.utils.translation import get_language_from_request
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from events.models import ForumEvent
from profile.models import Claim

#@login_required
##@permission_required('profile.change_claimevent')
#@render_to('admin/events/programm_manager_list.html')
#def events_programm_manager_list(request):
#    return dict(
#        claims = Claim.objects.filter(claim_state=CLAIM_ACCEPTED).order_by('last_name'),
#        manage_events=True,
#    )


@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/events/index.html')
def index(request):
    events = ForumEvent.objects.for_registration().distinct()
    return {'events': events}


@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/events/show.html')
def show(request, id):
    event = get_object_or_404(ForumEvent, id=id)
    return {'event': event}

#@login_required
#@user_passes_test(lambda u: u.is_staff)
#def events_change(request, id, printable=False):
#    event = get_object_or_404(Event, pk=id)
#    claims = ClaimEvent.objects.filter(event=event).order_by('claim__last_name')
#
#    template = 'admin/claims/events_edit.html'
#
#    if printable:
#        #template = 'admin/claims/list_print.html'
#        template = 'admin/claims/events_edit_print.html'
#
#    return render_to_response(template,
#        dict(
#            event = event,
#            claims = claims,
#            manage_events=True,
#        ), context_instance=RequestContext(request)
#    )

# --------------------------------------------------------------------------- #
