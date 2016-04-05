# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib import messages as django_messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import mail
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect

from openteam.utils import debug, send_email

from profile.models import Claim
from profile.utils import get_filtered_claims
from profile import settings as profile_settings



def send_notification(claim):
    email = claim.delegation_manager.email if claim.delegation_manager else claim.email
    send_email(email, 'request_info', { 'claim': claim })


class RequestAdditionalInfo(object):

    class ActionForm(forms.Form):
        action_code = forms.IntegerField(widget=forms.HiddenInput)

    PREFIX='request_info'

    MAKE_REQUEST = 1
    MARK_RECIEVED = 2
    REQUEST_INFO_ACTIONS = {
        MAKE_REQUEST: 'Запросить',
        MARK_RECIEVED: 'Получена',
    }

    REQUEST_ORDER = {
        profile_settings.REQUESTED_ABSENT: MAKE_REQUEST,
        profile_settings.REQUEST_SENT: MARK_RECIEVED,
        profile_settings.REQUEST_PROCESSED: None
    }

    NEXT_CODE = {
        MAKE_REQUEST:  { 'code': profile_settings.REQUEST_SENT, 'callback': send_notification },
        MARK_RECIEVED: { 'code': profile_settings.REQUEST_PROCESSED, 'callback': 'asd' },
    }


    def __init__(self, claim):
        self.claim = claim


    def get_action_form(self):
        next_request_action = self.REQUEST_ORDER[self.claim.additional_info]

        if next_request_action:
            title = self.REQUEST_INFO_ACTIONS[next_request_action]
            return {'title': title, 'form': self.ActionForm(initial={'action_code': next_request_action}, prefix=self.PREFIX)}

        return None


    def build_action_form(self, data):
        return self.ActionForm(data, prefix=self.PREFIX)


    def process_request(self, action_code):
        next_code = self.NEXT_CODE.get(action_code, None)

        if next_code:

            if next_code.get('callback', None):
                next_code.get('callback')(self.claim)

            self.claim.additional_info = next_code['code']
            self.claim.save()

            return True

        else:
            return False



class ParticipantRegistration(object):

    PREFIX = 'register'

    ACTION_TITLE = {
        True: u'Снять регистрацию',
        False: u'Зарегистрировать'
    }


    class ActionForm(forms.Form):
        is_registered = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, claim):
        self.claim = claim


    def get_action_form(self):
        is_registered = 0 if self.claim.is_registered else 1
        return {
            'title': self.ACTION_TITLE[self.claim.is_registered],
            'form': self.ActionForm(initial={'is_registered': is_registered}, prefix=self.PREFIX)
        }

    def build_action_form(self, data):
        return self.ActionForm(data, prefix=self.PREFIX)


    def process_action_form(self, post):
        action_form = self.build_action_form(post)

        if action_form.is_valid():
            self.claim.is_registered = action_form.cleaned_data['is_registered']
            self.claim.save()


class ParticipantInvitation(object):

    PREFIX = 'invite'

    ACTION_TITLE = {
        True: u'Не приглашать',
        False: u'Пригласить'
    }


    class ActionForm(forms.Form):
        is_invited = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, claim):
        self.claim = claim


    def get_action_form(self):
        is_invited = 0 if self.claim.is_invited else 1
        return {
            'title': self.ACTION_TITLE[self.claim.is_invited],
            'form': self.ActionForm(initial={'is_invited': is_invited}, prefix=self.PREFIX)
        }

    def build_action_form(self, data):
        return self.ActionForm(data, prefix=self.PREFIX)


    def process_action_form(self, post):
        action_form = self.build_action_form(post)

        if action_form.is_valid():
            self.claim.is_invited = action_form.cleaned_data['is_invited']
            self.claim.save()




@login_required
@user_passes_test(lambda u: u.is_staff)
def request_process(request, id):
    claim = get_object_or_404(Claim, id=id)

    if request.method == 'POST':
        form = RequestAdditionalInfo(claim).build_action_form(request.POST)

        if form.is_valid():
            additional_info_request = RequestAdditionalInfo(claim)
            additional_info_request.process_request(form.cleaned_data['action_code'])

    return redirect(request.META.get('HTTP_REFERER', reverse('manage_claim_list')))


@login_required
@user_passes_test(lambda u: u.is_staff)
def registration_process(request, id):
    claim = get_object_or_404(Claim, id=id)

    if request.method == 'POST':
        ParticipantRegistration(claim).process_action_form(request.POST)

    django_messages.success(request, 'Регистрация изменена')

    return redirect(request.META.get('HTTP_REFERER', reverse('manage_claim_list')))


@login_required
@user_passes_test(lambda u: u.is_staff)
def invitation_process(request, id):
    claim = get_object_or_404(Claim, id=id)

    if request.method == 'POST':
        ParticipantInvitation(claim).process_action_form(request.POST)

    django_messages.success(request, 'Приглашение изменено')

    return redirect(request.META.get('HTTP_REFERER', reverse('manage_claim_list')))



@login_required
@user_passes_test(lambda u: u.is_staff)
def email_mass_send(request):
    from profile.forms import EmailMessageForm
    message_form = EmailMessageForm(request.POST or None)

    def get_messages(claims, subject, body):
        messages = []
        connection = mail.get_connection(fail_silently=True)
        for claim in claims:
            if claim.email:
                recipient = ['<%s>' % claim.email,]
                messages.append(mail.EmailMessage(subject=subject, body=body,
                                                    from_email=settings.DEFAULT_FROM_EMAIL,
                                                    to=recipient, connection=connection))
            else:
                print claim
        return messages

    if message_form.is_valid():
        filters = request.session.get('filter_data', dict())
        claims, filter_set = get_filtered_claims(filters)
        subject = message_form.cleaned_data['subject']
        body = message_form.cleaned_data['body']
        body += u"""
---
С уважением,
Организационный комитет
XIV Томский инновационный форум INNOVUS
http://innovus.biz/
"""
        messages = get_messages(claims, subject, body)
        for message in messages:
            try:
                response = message.send()
                debug(response)
            except Exception, e:
                debug(e)
        django_messages.success(request, 'Сообщение отправлено')
        return redirect('manage_claim_list')

    django_messages.error(request, 'Сообщение не отправлено')
    return redirect('manage_claim_list')


