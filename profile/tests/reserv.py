# -*- coding: utf-8 -*-

from datetime import datetime
from django.test import TestCase, client
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from profile import CLAIM_SENT, CLAIM_WAITING_APPROVEMENT, \
    CLAIM_WAITING_PAYMENT, CLAIM_ACCEPTED, CLAIM_CANCELLED, CLAIM_REJECTED
from profile.tests import get_full_valid_data
from profile.forms import ClaimForm
from profile.models import Claim, Hotel, HotelRoomCategory, HotelRoomReserve

class ReserveTest(TestCase):
    def create_claim(self, email=None):
        data = get_full_valid_data()
        if email:
            data['email'] = email

        return ClaimForm(data).save()

    def setUp(self):
        # Create superuser
        self.superuser = User.objects.create_superuser('demo', 'demo@demo.de', 'demo')
        self.client = client.Client()
        self.client.login(username='demo', password='demo')

        # Create hotel
        self.hotel = Hotel.objects.create(name='Paradise')

        # Create room category
        self.room = HotelRoomCategory.objects.create(
            hotel         = self.hotel,
            room_category = 1,
            room_number   = 1,
            price         = 1500,
            is_real_room  = True,
        )


#    def test_reserve_delegation_manager_email(self):
#        mail.outbox=[]
#
#        manager = self.create_claim('manager@manager.mg')
#
#        claim    = self.create_claim()
#        claim.delegation_manager = manager
#        claim.save()
#
#        url   = reverse('manage_reserv_add', kwargs=dict(id = claim.id))
#
#        resp = self.client.get(url)
#        self.assertEquals(200, resp.status_code)
#
#        resp = self.client.post(url, dict(
#            hotel          = self.hotel.id,
#            room_class     = self.room.room_category,
#            room_number    = self.room.room_number,
#            arrival_date   = '20.05.2010 16:40',
#            departure_date = '29.05.2010 16:40',
#        ))
#
#        self.assertEquals(302, resp.status_code)
#
#        found=False
#        for message in mail.outbox:
#            if message.subject == render_to_string('profile/email/reserv/add_delegation_manager.subj.html'):
#                self.assertTrue('<%s>'%manager.email in message.to)
#                found=True
#                break
#
#        if not found:
#            self.fail('no messages found')
#
#    def test_reserve_claim_email(self):
#        mail.outbox=[]
#        claim = self.create_claim()
#        url   = reverse('manage_reserv_add', kwargs=dict(id = claim.id))
#
#        resp = self.client.get(url)
#        self.assertEquals(200, resp.status_code)
#
#        resp = self.client.post(url, dict(
#            hotel          = self.hotel.id,
#            room_class     = self.room.room_category,
#            room_number    = self.room.room_number,
#            arrival_date   = '20.05.2010 16:40',
#            departure_date = '29.05.2010 16:40',
#        ))
#
#        self.assertEquals(302, resp.status_code)
#
#        found = False
#        for message in mail.outbox:
#            if message.subject == render_to_string('profile/email/reserv/add_claim.subj.html'):
#                found=True
#                self.assertTrue('<%s>'% claim.email in message.to )
#                break
#
#        if not found:
#            self.fail('no messages found')

    # ----------------------------------------------------------------------- #

    def test_remove_reserve_if_claim_is_rejected(self):
        claim = self.create_claim()
        HotelRoomReserve.objects.create(
            room  = self.room,
            claim = claim,
            arrival_date   = datetime.now(),
            departure_date = datetime.now(),
        )

        claim.claim_state = CLAIM_REJECTED
        claim.save()

        def raise_exception():
            HotelRoomReserve.objects.get(room=self.room, claim=claim)

        self.assertRaises(HotelRoomReserve.DoesNotExist, raise_exception)

    def test_remove_reserve_if_claim_is_cancelled(self):
        claim = self.create_claim()
        HotelRoomReserve.objects.create(
            room  = self.room,
            claim = claim,
            arrival_date   = datetime.now(),
            departure_date = datetime.now(),
        )

        claim.claim_state = CLAIM_CANCELLED
        claim.save()

        def raise_exception():
            HotelRoomReserve.objects.get(room=self.room, claim=claim)

        self.assertRaises(HotelRoomReserve.DoesNotExist, raise_exception)


    def test_no_remove_reserve_if_claim_is_not_rejected_or_cancelled(self):
        claim = self.create_claim()
        HotelRoomReserve.objects.create(
            room  = self.room,
            claim = claim,
            arrival_date   = datetime.now(),
            departure_date = datetime.now(),
        )

        states = [
            CLAIM_SENT, CLAIM_WAITING_APPROVEMENT, CLAIM_WAITING_PAYMENT,       \
            CLAIM_ACCEPTED,
        ]

        for state in states:
            claim.claim_state = state
            claim.save()
            self.assertEquals(1, HotelRoomReserve.objects.filter(room=self.room, claim=claim).count())

