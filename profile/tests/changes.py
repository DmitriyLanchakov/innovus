# -*- coding: utf-8 -*-

from datetime import datetime
from time import strptime
from profile.tests import TestCase, get_full_valid_data
from profile.forms import ClaimForm
from profile.models import Claim, History

# --------------------------------------------------------------------------- #

class ClaimChangeTest(TestCase):
    def setUp(self):
        form = ClaimForm(get_full_valid_data())
        form.is_valid()       
        self.claim = form.save()

    def test_synchronized_by_default(self):
        self.assertTrue(self.claim.is_synchronized)
        
    def test_synchronzed_if_edit_unimportant_fields(self):
        self.claim.first_name = 'Foo'
        self.claim.save()
        self.assertTrue(self.claim.is_synchronized)

    def test_synchronze_model_method(self):
        self.claim.is_synchronized = False
        self.claim.synchronize()
        self.assertTrue(self.claim.is_synchronized)
   
    def test_not_synchronzed_if_changes_arrival_want_charter(self):
        self.not_synchronzed_if_changes('arrival_want_charter', True)

    def test_not_synchronzed_if_changes_departure_want_charter(self):
        self.not_synchronzed_if_changes('departure_want_charter', True)


    def test_not_synchronzed_if_changes_arrival_transport_type(self):
        self.not_synchronzed_if_changes('arrival_transport_type', 2)

    def test_not_synchronzed_if_changes_departure_transport_type(self):
        self.not_synchronzed_if_changes('departure_transport_type', 2)

    def test_not_synchronzed_if_changes_arrival_date(self):
        self.not_synchronzed_if_changes('arrival_date', datetime(*strptime('2010-05-26 14:00:00', '%Y-%m-%d %H:%M:%S')[:6]))

    def test_not_synchronzed_if_changes_departure_date(self):
        self.not_synchronzed_if_changes('departure_date', datetime(*strptime('2010-05-27 14:00:00', '%Y-%m-%d %H:%M:%S')[:6]))

    def test_not_synchronzed_if_changes_room_category(self):
        self.not_synchronzed_if_changes('room_category', 1)

    def not_synchronzed_if_changes(self, field, new_value):
        #print field, "=>", self.claim.is_synchronized
        self.assertTrue(self.claim.is_synchronized)
        setattr(self.claim, field, new_value)
        self.claim.save()
        self.assertFalse(self.claim.is_synchronized)
