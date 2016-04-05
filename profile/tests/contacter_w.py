# -*- coding: utf-8 -*-

from time import strptime 
from django.test import client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from profile.tests import TestCase, get_full_valid_data
from profile.models import *
from profile.forms import *

# --------------------------------------------------------------------------- #

def get_valid_contacter_data():
    data = get_full_valid_data()
    data['is_take_part'] = str(TAKE_PART_CONTACT_W_P)
    return data

# --------------------------------------------------------------------------- #
#'2010-05-19 14:00:00'
class ContacterWithParticipateViewTest(TestCase):
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
        self.assertEquals(4, claim.arrival_transport_type)
        self.assertEquals(4, claim.departure_transport_type)
        self.assertNotEquals(None, claim.arrival_date)
        self.assertNotEquals(None, claim.departure_date)
        self.assertEquals(2, claim.room_category)

    def test_registration_fail(self):
        data = get_valid_contacter_data()

        del data['departure_want_charter']
        
        resp = self.browser('add_contact', data)
        form = resp.context['claim_form']
        
        self.assertEquals(200, resp.status_code)
        self.assertFalse(form.is_valid())
        self.assertTrue('departure_want_charter' in form._errors)
        
        

 
