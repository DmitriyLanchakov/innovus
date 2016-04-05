from django.contrib import messages
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext as _

from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from openteam.utils import send_email

from profile.decorators import works_in
from profile.models import Claim
from profile import settings as profile_settings


@works_in(settings.REG_START, settings.REG_END)
@render_to('profile/activation.html')
def activation(request, code=None):
    if not code:
        code = request.GET.get('code', None)

    if request.user.is_authenticated() or request.method == 'POST':
        return redirect('profile_view')

    if code:
        claim = get_object_or_None(Claim, activation_code=code)

        if not claim:
            return {'fail': _('Activation code invalid.')}

        elif claim.user.is_active:
            return {'fail': _('Claim has been already activated.')}

        elif claim.activate():
            send_email(settings.NOTIFY_EMAIL, 'notice', {'claim': claim, 'action': 'activation'})
            claim.user.backend = 'django.contrib.auth.backends.ModelBackend'
            django_login(request, claim.user)

        else:
            return {'fail': _('Activation failed.') }

    return {}


@login_required
@render_to('profile/claim_forms/claim_delete.html')
def cancel(request, id=None):
    if id is None:
        claim = get_object_or_404(Claim, user=request.user)
    else:
        claim = get_object_or_404(Claim, id=id, delegation_manager=request.user.get_profile())

    if request.POST:
        claim.is_deleted = True
        claim.claim_state = profile_settings.CLAIM_CANCELLED
        claim.save()
        messages.success(request, _('Claim cancelled'))

        return redirect('profile_view')

    return {'claim': claim}


@login_required
def get_bill(request, id):
    claim = get_object_or_404(Claim, pk=id)
    if request.user.is_staff or \
        (claim.user and request.user == claim.user) or \
        (claim.delegation_manager and request.user == claim.delegation_manager.user):
        response = HttpResponse(claim.get_bill(request), mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=payment_bill.pdf'
        return response
    else:
        raise Http404
