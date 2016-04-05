# -*- coding: utf-8 -*-
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase, client

from profile.models import Claim
from profile.views.actions import RequestAdditionalInfo

class TestManagementActions(TestCase):
    fixtures = ['users.json', 'claims.json']



    def setUp(self):
        self.client = client.Client()
        self.client.login(username='demo', password='OTr206Mkr0tomskforum')


    def testRequestAdditionalInfo(self):
        claim = Claim.objects.all().order_by('?')[0]
        previous_info = claim.additional_info

        next_request_action = RequestAdditionalInfo.REQUEST_ORDER[claim.additional_info]
        data = {'request_info-action_code': next_request_action }

        emails_before = len(mail.outbox)
        response = self.client.post(reverse('actions_request_process', kwargs={'id': claim.id}), data, follow=False)
        emails_before += 2

        self.assertEquals(len(mail.outbox), emails_before)

