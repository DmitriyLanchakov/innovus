'''
Created on 29.04.2010

@author: nimnull
'''
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from annoying.decorators import render_to
from openteam.utils import send_email

from profile.decorators import works_in
from profile.forms import ClaimForm
from profile.models import Claim
from profile import settings as profile_settings


@works_in(settings.REG_START, settings.REG_END)
@login_required
@render_to('profile/claim_forms/join_delegate.html')
def add(request):
    form = ClaimForm(request.POST or None)
    if form.is_valid():
        delegate = form.save(commit = False)
        delegate.delegation_manager = request.user.get_profile()
        delegate.claim_state = profile_settings.CLAIM_WAITING_APPROVEMENT
        delegate.save()
        messages.success(request, _('Delegate succsessfully added'))
        send_email(settings.NOTIFY_EMAIL, 'notice', {'claim': delegate, 'action': 'registration'})
        return redirect('list_delegate')
    else:
        if form.is_bound:
            messages.error(request, _('Delegate creation failed'))
        print form.errors
    vt = _('Add new delegate')
    return dict(
        delegates = request.user.get_profile().delegates,
        claim_form = form,
        view_title = vt,
        is_delegate_list= True,
        claim = request.user.get_profile(),
        )

@login_required
@render_to('profile/claim_forms/join_delegate.html')
def edit(request, id):
    delegate = get_object_or_404(Claim,
        delegation_manager=request.user.get_profile(),
        pk=id
    )
    if request.method == 'POST':
        form = ClaimForm(request.POST, instance=delegate)
        if form.is_valid():
            delegate = form.save()
            messages.success(request, _('Delegate changed'))
            return redirect('show_delegate', id=delegate.pk)
        else:
            messages.error(request, _('Delegate edition failed'))
    else:
        form = ClaimForm(instance=delegate)
    vt = _('Delegation management')
    return dict(
        delegate = delegate,
        claim_form = form,
        view_title = vt,
        delegates = request.user.get_profile().delegates,
        is_delegate_list = True,
    )

# --------------------------------------------------------------------------- #

@login_required
@render_to('profile/delegate_list.html')
def list(request):
    claim = request.user.get_profile()

    if claim.is_take_part == profile_settings.TAKE_PART_CONTACT_WO_P:
        delegates = claim.delegates

    else:
        delegates = Claim.objects.filter( Q(pk = claim.pk) | Q(pk__in = claim.delegates.values('id')))

    return dict(
        claim = claim,
        delegates = delegates.order_by('last_name','first_name','middle_name'),
        is_delegate_list = True,
    )


@login_required
@render_to('profile/delegate_show.html')
def show(request, id):
    if int(id) == request.user.get_profile().id:
        return redirect('profile_view')

    claim = request.user.get_profile()
    delegate = get_object_or_404(Claim,
        delegation_manager=claim,
        pk=id,
    )

    return dict(
        claim = claim,
        delegate = delegate,
        delegates = claim.delegates,
        is_delegate_list = True,
    )


@login_required
@render_to('profile/claim_forms/delegate_delete.html')
def delete(request, id):
    delegate = get_object_or_404(Claim,
        delegation_manager=request.user.get_profile(),
        pk=id
    )

    if request.method == 'POST':
        delegate.is_deleted = True
        delegate.save()
        messages.success(request, _('Delegate deleted'))

        return redirect('profile_view')

    return dict(
        delegate = delegate
    )

