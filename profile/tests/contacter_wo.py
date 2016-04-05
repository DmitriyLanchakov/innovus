# -*- coding: utf-8 -*-

from django.test import TestCase, client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from profile.tests import get_full_valid_data
from profile.models import *
from profile.forms import *

# --------------------------------------------------------------------------- #

def get_valid_contacter_data():
    data = get_full_valid_data()
    data['is_take_part'] = str(TAKE_PART_CONTACT_WO_P)
    return data

# --------------------------------------------------------------------------- #

class ContacterWithoutParticipateFormTest(TestCase):
    def test_(self):
        data = get_valid_contacter_data()

        non_required = [
            'room_category',
            'arrival_date', 'arrival_want_charter', 'arrival_transport_type',
            'departure_date', 'departure_want_charter', 'departure_transport_type',
        ]

        for i in non_required:
            data.pop(i)
            form = ClaimForm(data)
            self.assertTrue(form.is_valid())

# --------------------------------------------------------------------------- #

class ContacterWithoutParticipateViewTest(TestCase):
    def setUp(self):
        self.client = client.Client()

    def browser(self, view, data):
        url  = reverse(view)
        self.client.get(url)
        return self.client.post(url, data)

    def test_registration_ok(self):
        resp = self.browser('join_contact', get_valid_contacter_data())

        self.assertEquals(302, resp.status_code)
        self.assertEquals(1, User.objects.count())
        
        claim = User.objects.all()[0].get_profile() 

        self.assertEquals(0, claim.arrival_want_charter)
        self.assertEquals(0, claim.departure_want_charter)
        self.assertEquals(None, claim.arrival_transport_type)
        self.assertEquals(None, claim.departure_transport_type)
        self.assertEquals(None, claim.arrival_date)
        self.assertEquals(None, claim.departure_date)
        self.assertEquals(0, claim.room_category)
 
    def test_registration_null_data(self):
        data = get_valid_contacter_data()
        data['arrival_want_charter'] = '1'
        data['departure_transport_type'] = '2'
        data['need_hotel'] = '1'       
               
        resp = self.browser('join_contact', data)

        self.assertEquals(302, resp.status_code)
        self.assertEquals(1, User.objects.count())
        
        claim = User.objects.all()[0].get_profile() 

        self.assertEquals(0, claim.arrival_want_charter)
        self.assertEquals(None, claim.departure_transport_type)
        self.assertEquals(0, claim.room_category)
        
 
 
