# -*- coding: utf-8 -*-

from django.core import urlresolvers
from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse


from haystack.query import SearchQuerySet

from periodics.models import Post, Category


class TestFocus(TestCase):

    def setUp(self):
        self.sqs = SearchQuerySet()
        self.post = Post.objects.create(
            title = u'Продолжается конкурс молодежных инновационных проектов',
            slug = 'adasdasdssss',
            annotation = u'Продолжается конкурс молодежных инновационных проектов',
            content = 'В этом году награждение победителей будет проходить по 8 номинациям',
        )

        self.category = Category.objects.create(title='test')
        self.category.posts.add(self.post)
        self.post.publish()


    def testLikeness(self):
        sqs = SearchQuerySet().more_like_this(self.post.publisher_public)
        self.assertNotEqual(0, sqs.count())

