from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from annoying.decorators import render_to
from annoying.functions import get_object_or_None
import claim
from profile.decorators import works_in
from profile.forms import ClaimForm, StateForm
from profile.models import Claim
from profile import filters, settings as profile_settings


@works_in(settings.REG_START, settings.REG_END)
def add(request):
    return claim.add(request, template='profile/claim_forms/join.html', type='participant')


@login_required
@render_to('profile/claim_forms/edit_claim.html')
def edit(request):
    view_title = _('Edit claim')
    claim = get_object_or_None(Claim, user=request.user)

    claim_form = ClaimForm(request.POST or None, instance=claim, context='edit')

    if claim_form.is_valid():
        claim_form.save()
        messages.success(request, _('Claim updated successfully'))
        return redirect('profile_view')

    return dict(
        claim    = claim,
        claim_form = claim_form,
        view_title = view_title,
        delegates = Claim.objects.filter( Q(pk = claim.pk) | Q(pk__in = claim.delegates.values('id'))),
        is_profile_view = True,
    )


@login_required
@render_to('profile/view.html')
def view(request):
    view_title = _('View profile')
    claim = get_object_or_None(Claim, user=request.user)
    if not claim:
        return redirect('/')
    delegates = Claim.objects.filter(delegation_manager=request.user.get_profile())

    return {'claim': claim,
            'view_title': view_title,
            'delegates': delegates,
            'is_profile_view': True}

