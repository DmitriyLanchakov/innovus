# -*- coding: utf-8 -*-
'''
Created on 30.04.2010

@author: nimnull
'''
from django.test import TestCase, client
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth.models import User
from django.db.models import Q

from profile.utils import ACTION_RESEND_ACTIVATION, ACTION_RESEND_RESERVATION
from profile.models import Claim, HotelRoomReserve

class TestDelivery(TestCase):
    fixtures = ['users.json', 'claims.json', 'reserve.json']

    def setUp(self):
        self.client = client.Client()
        self.client.login(username='demo', password='OTr206Mkr0tomskforum')
        self.staff  = User.objects.filter(is_staff=True)[0] if User.objects.filter(is_staff=True).count() else None

    def tearDown(self):
        pass


    def testResendActivation(self):
        data = {'action_code': ACTION_RESEND_ACTIVATION }
        response = self.client.post(reverse('management_action_process'), data, follow=False)
        self.assertEquals(response.status_code, 302)
        self.assertNotEquals(len(mail.outbox), 0)


    def testMassDelivery(self):
        data = {'subject': 'test', 'body': 'testqwerty' }
        claims_count = Claim.objects.count()
        response = self.client.post(reverse('actions_email_mass_send'), data)
        self.assertNotEquals(len(mail.outbox), 0)
        self.assertEquals(mail.outbox[0].subject, 'test')


    def testResendReservation(self):
        hosted = [i['claim'] for i in HotelRoomReserve.objects.values('claim')]
        claim = Claim.objects.filter(
            Q(room_category__isnull = False) & \
            Q(room_category__gt     = 0)
        ).filter(pk__in=hosted).order_by('?')[0]
        data = {'action_code': ACTION_RESEND_ACTIVATION, 'claim_id': claim.id }
        response = self.client.post(reverse('management_action_process'), data, follow=False)
        self.assertEquals(response.status_code, 302)
        self.assertNotEquals(len(mail.outbox), 0)
        self.assertEquals(mail.outbox[0].subject, 'Информация о заселении в гостиницу')



    def testChangeState(self):
        participants = Claim.objects.filter(
            delegation_manager__isnull = True,
            user__isnull = False,
        ).order_by('?')

        participant = participants[0]

        delegates = Claim.objects.filter(
            delegation_manager__isnull = False,
            user__isnull = True,
        ).order_by('?')

        delegate = delegates[0]

        next_states_p = participant.next_states
        next_states_d = delegate.next_states

        data_p = {'new_state': next_states_p[0] }
        response = self.client.post(reverse('manage_state_change', kwargs={'id': participant.id}), data_p)
        p = Claim.objects.get(pk = participant.id)

        self.assertEquals(p.claim_state, data_p['new_state'])

        data_d = {'new_state': next_states_d[0] }
        response = self.client.post(reverse('manage_state_change', kwargs={'id': delegate.id}), data_d)
        d = Claim.objects.get(pk = delegate.id)

        self.assertEquals(d.claim_state, data_d['new_state'])

