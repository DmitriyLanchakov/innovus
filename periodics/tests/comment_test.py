# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core import urlresolvers
from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from periodics.forms import CommentForm
from periodics.models import *

def set_up_category():
    return Category.objects.create(title = 'Test', )

def set_up_user():
    return User.objects.create_user(
        username  = 'test_auth',
        email     = 'test@mydomain.com',
        password  = 'test',
    )

def set_up_post():
    set_up_category()

    return Post.objects.create(
        title   = 'Test post',
        slug    = 'test_post',
        content = 'This is a test post, so hello and jazz.'
    )

def set_up_comment(test_author, test_post):
    return Comment.objects.create(
        author      = test_author,
        commentable = test_post,
        ip_address  = '127.0.0.1',
        content     = 'This is a test comment on test post'
    )

# --------------------------------------------------------------------------- #

class TestAuthor(TestCase):
    def setUp(self):
        self.test_user = set_up_user()
        self.anon_author = AnonAuthor.objects.create(name="test_anon", email="test@mail.com")
        self.auth_author = AuthAuthor.objects.create(user=self.test_user)
        self.open_author = OpenIDAuthor.objects.create(openid="http://test.openid.org", name="test_open", email="test@openid.org")

    def testAnonInheritance(self):
        self.assertTrue(isinstance(self.anon_author, Author))

    def testAuthInheritance(self):
        self.assertTrue(isinstance(self.auth_author, Author))

    def testOpenInheritance(self):
        self.assertTrue(isinstance(self.open_author, Author))

# --------------------------------------------------------------------------- #

class TestCommenting(TestCase):
    def setUp(self):
        self.test_user = set_up_user()
        self.auth_author = AuthAuthor.objects.create(user = self.test_user)

        self.category = set_up_category()
        self.post = set_up_post()

        self.comment1 = set_up_comment(self.auth_author, self.post)
        self.comment2 = set_up_comment(self.auth_author, self.post)
        self.comment3 = set_up_comment(self.auth_author, self.post)

    def testComments(self):
        self.assertEquals(3, Comment.objects.count())

    def testCommentsRoot(self):
        self.comment1.move_to(None)
        self.assertTrue(self.comment1 in Comment.tree.root_nodes())

    def testCommentsLeaf(self):
        self.comment3.move_to(self.comment2)
        self.comment2.move_to(self.comment1)
        self.comment1 = Comment.objects.get(pk=self.comment1.pk)
        self.assertEquals(1, self.comment1.get_children().count())

# --------------------------------------------------------------------------- #

class TestCommentForms(TestCase):
    def setUp(self):
        self.user = set_up_user()
        self.post = set_up_post()

        self.form_data = {'comment-content': "test comment content", 'comment-post': self.post.pk }
        self.with_openid = {'openid-openid': "egorrkin.ya.ru"}
        self.with_openid.update(self.form_data)
        self.with_anonymous = {'anon-name': 'somebody', 'anon-email': 'mail@mail.com' }
        self.with_anonymous.update(self.form_data)

        self.c = Client()
        self.comment_post_url = urlresolvers.reverse("comment-add")

    def testCommentFormValidation(self):
        form = CommentForm(self.form_data, prefix="comment")
        self.assertTrue(form.is_valid())
    
    def testOpenIDCommentPosting(self):
        pass

# --------------------------------------------------------------------------- #

class TestPremoderated(TestCase):
    def setUp(self):
        self.user = set_up_user()
        self.post = set_up_post()
        self.author = AuthAuthor.objects.create(user=self.user)

        self.comment = set_up_comment(self.author, self.post)
        self.comment.is_approved = True
        self.comment.save()

    def testCountUnapproved(self):
        self.comment.is_approved = False
        self.comment.save()
        self.assertEquals(1, Comment.objects.count())
        self.assertEquals(0, Comment.objects.approved().count())
        
    def testCountApproved(self):
        self.assertEquals(1, Comment.objects.count())
        self.assertEquals(1, Comment.objects.approved().count())

    def testCountUnapproved2(self):
        self.comment.is_approved = False
        self.comment.save()

        self.assertEquals(0, Comment.objects.approved().count())
        self.comment.approve()
        self.assertEquals(1, Comment.objects.approved().count())
        self.assertEquals(1, Comment.objects.count())        
        

