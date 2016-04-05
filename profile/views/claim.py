from annoying.decorators import render_to
from django.contrib.auth.models import User
from django.shortcuts import redirect
from openteam.utils import send_email
from profile.decorators import works_in
from profile.forms import ClaimForm
from django.conf import settings


@works_in(settings.REG_START, settings.REG_END)
@render_to()
def add(request, template, type='participant'):
    claim_form = ClaimForm(request.POST or None)
    if claim_form.is_valid():
        user  = User.objects.create_user(
            username = claim_form.cleaned_data['email'],
            password = claim_form.cleaned_data['password'],
            email    = claim_form.cleaned_data['email'],
        )
        user.first_name = claim_form.cleaned_data['first_name']
        user.last_name = claim_form.cleaned_data['last_name']
        user.is_active = False
        user.save()
        claim = claim_form.save(commit=False)
        claim.user = user
        claim.save()
        send_email(user.email, 'registration', {'code': claim.activation_code } )
        send_email(settings.NOTIFY_EMAIL, 'notice', {'claim': claim, 'action': 'registration'})
        return redirect('join_%s_complete' % type)
    return {'claim_form': claim_form, 'TEMPLATE': template}

