# -*- coding: utf-8 -*-

from django import forms
from django.db import models
from django.core import exceptions, urlresolvers
from django.test import TestCase, client
from django.utils import simplejson
from django.contrib.auth.models import User
from periodics.models import Category, Post

# ---------------------------------------------------------------------------- #

class AjaxFormTest(TestCase):
    def setUp(self):
        self.client    = client.Client()
        self.post_data = {}
        self.url       = '/'
        self.auth = {'username': 'root', 'password': 'root', 'email': 'm@m.ru',}
        self.root = User.objects.create_user(
            username = self.auth['username'],
            password = self.auth['password'],
            email    = self.auth['email'],
        )

        self.post_data = {
            'content'  : 'Post content',
            'category' : Category.objects.create(title='Test').pk,
            'title'    : 'Post #1',
            'slug'     : 'post-1',
            'is_active': True,           
        }

        self.root.is_staff = True
        self.root.is_superuser = True
        self.root.save() 

    def tearDown(self):
        for i in [Post, Category, User]:
            clean = i.objects.all()
            clean.delete()

    def root_login(self):
        self.client.login(
            username = self.auth['username'],
            password = self.auth['password'],
        )

    def ajax_post(self):
        return self.client.post(
            self.url,
            self.post_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

    def get_json(self):
        return simplejson.loads(self.ajax_post().content)

# --------------------------------------------------------------------------- #

class CategoryTest(AjaxFormTest):
    def setUp(self):
        super(CategoryTest, self).setUp()              
        self.url = urlresolvers.reverse('add-category')
        self.post_data = {'title': 'FooCategory', 'per_page':10,}
        self.root_login()

    def tearDown(self):
        super(CategoryTest, self).tearDown()
        self.client.logout()

    def testPermissionDenied(self):
        self.client.logout()
        resp = self.client.post(self.url)
        self.assertEquals(403, resp.status_code)

    def testCreateCategoryWithoutPost(self):
        cats = Category.objects.all()
        cats.delete()

        self.assertEquals(0, Category.objects.count())
        self.assertEquals(0, Post.objects.count())

        json = self.get_json()

        self.assertEquals(1, Category.objects.count())
        self.assertEquals(0, Post.objects.count())        
        
    def testAddCategoryToPost(self):
        # First of all create post...
        post = Post.objects.create(
            title = 'Test post',
            slug  = 'test-post',
            is_active = True,              
        )        

        # ...which hasn't any categories...
        self.assertEquals(0, post.category.count())        
        
        # Compile URL to create category...
        self.url = urlresolvers.reverse('add-category',
            kwargs={
                'post_id': post.pk
            }
        )
        # ...and make AJAX request
        json = self.get_json()
        
        # Test
        self.assertEquals(1, post.category.count())
        self.assertEquals(self.post_data['title'], json['category']['title'])