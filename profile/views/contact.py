from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ungettext_lazy as _

from annoying.decorators import render_to
import claim
from profile.decorators import works_in

from profile.forms import ClaimForm
from profile.models import Claim

@works_in(settings.REG_START, settings.REG_END)
def add(request):
    return claim.add(request, template='profile/claim_forms/join_contact.html', type='contact')

# --------------------------------------------------------------------------- #

@login_required
@render_to('profile/claim_forms/join_contact.html')
def edit(request, id):
    contact = get_object_or_404(Claim, pk=id)
    form = ClaimForm(request.POST or None, instance=contact)
    if form.is_valid():
        form.save()
        messages.success(request, _('Delegate succsessfully added'))
        return redirect('profile_view')
    return dict(claim_form=form)
