# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import TestCase

from pysolr import Solr, SolrError

from indexer.utils import get_solr_tagcloud

class TestTags(TestCase):

    def setUp(self):
        self.solr = Solr(settings.HAYSTACK_SOLR_URL)


    def testTagCloud(self):
        cloud = get_solr_tagcloud()

        for key, value in cloud.items():
            print key, value

        self.assertNotEqual(0, len(cloud)) 
