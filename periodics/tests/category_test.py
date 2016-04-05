# -*- coding: utf-8 -*-

from django.test.client import Client
from django.test import TestCase
from django.contrib.auth.models import User

from periodics.models import Category


class CategoryTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title = "Test category")


    def testCreatedBy(self):
        """Test if category was created by script
        """
        self.assertEqual(self.category.created_by, "script")


    def testModificationAttributes(self):
        """Test if category modification date has been updated
        """
        new_title = "Modified title"
        modification_date = self.category.modified_at
        self.category.title = new_title
        self.category.save()

        self.assertEqual(self.category.title, new_title)
        self.assertNotEqual(self.category.modified_at, modification_date)

