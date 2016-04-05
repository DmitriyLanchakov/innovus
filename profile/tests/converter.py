# -*- coding: utf-8 -*-

from datetime import datetime
from django.test import TestCase, client
from profile.models import Claim
from profile.utils import generate_bill

class TestConverter(TestCase):
    fixtures = ['users.json', 'claims.json']



    def testConvert(self):
        claim = Claim.objects.all().order_by('?')[0]
        self.assertNotEquals(claim.get_bill, None)

    def test_convert_date_created(self):
        claim = Claim.objects.all().order_by('?')[0]
        
        self.assertTrue(claim.bill_date is None)        
        self.assertNotEquals(claim.get_bill, None)
        self.assertNotEquals(claim.bill_date, None)
        self.assertTrue(datetime.now() > claim.bill_date)
 
