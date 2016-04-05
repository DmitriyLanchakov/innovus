# -*- coding: utf-8 -*-

from django.core import urlresolvers
from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse

from haystack.forms import HighlightedSearchForm
from haystack.query import SearchQuerySet


class TestSearch(TestCase):


    def setUp(self):
        self.query = {'q': 'томск' }
        self.client = Client()


#    def testSearch(self):
#        form = HighlightedSearchForm(self.query)
#        sqs = form.search()
#        self.assertNotEqual(len(sqs), 0)


#    def testSearchResultsPage(self):
#        response = self.client.get(reverse('haystack_search'), self.query)
#        self.assertNotEqual(len(response.context['page'].object_list), 0)

