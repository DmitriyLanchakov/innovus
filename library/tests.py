# encoding: utf-8
from django.test import TestCase
from .plugins.models import PersonsList


class SimpleTest(TestCase):

    def setUp(self):
        pass

    def test_dummy(self):
        print PersonsList._meta.db_table
        self.assertEqual(1, True)

