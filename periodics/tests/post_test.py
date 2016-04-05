# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.test import TestCase, client
from django.core import exceptions, urlresolvers
from django.contrib.auth.models import User
from django.utils import simplejson
from publisher.models import Publisher
from periodics.models import PeriodicsBase, Post, Category
from periodics.tests.comment_test import set_up_user, set_up_post

# --------------------------------------------------------------------------- #

class PostTest(TestCase):
    def setUp(self):
        """
        Prepare test environment
        """
        # Post instance template (must be filled correctly)
        self.post = Post(
            title = 'Lorem ipsum',
            slug  = 'lorem-ipsum',
        )

        # Clean all posts before testcase runs
        to_delete = Post.objects.all()
        to_delete.delete()

        # Prepare datetimes
        self.day_today     = datetime.today()
        self.day_tomorrow  = self.day_today + timedelta(1)
        self.day_yesterday = self.day_today - timedelta(1)

    # ----------------------------------------------------------------------- #
    def testPublisherDraft(self):
        ''
        #self.post.save()
        #self.assertEquals(0, Post.objects.count())


    # ----------------------------------------------------------------------- #

    def testIsExpired(self):
        self.post.public_till = self.day_yesterday
        self.post.public_from = self.post.public_till - timedelta(1)
        self.post.save()
        #self.post.publish()
        self.assertTrue(self.post.is_expired)

        self.post.public_till = self.day_tomorrow
        self.post.save()
        self.assertFalse(self.post.is_expired)

        self.post.public_till = None
        self.post.save()
        self.assertFalse(self.post.is_expired)

    def testIsScheduled(self):
        self.post.public_from = self.day_tomorrow
        self.post.save()
        #self.post.publish()
        self.assertTrue(self.post.is_scheduled)

        self.post.public_from = self.day_yesterday
        self.post.save()
        self.assertFalse(self.post.is_scheduled)

    #------------------------------------------------------------------------ #

    def testByDateFilter(self):
        year = 2010

        month_number = 3
        post_per_month = 4

        # Test dump
        for month in range(1, month_number + 1):
            for day in range(1, post_per_month + 1):
                p = Post(
                    title = 'Post %s' % month * day,
                    slug  = 'post-%s' % month * day,
                    public_from = '%d-%02d-%02d' % (year, month, day),
                )
                p.save()
                #p.publish()

        # The only post for current date: 2010-01-01
        self.assertEquals(1,
            Post.objects.by_date(
                year = year,
                month = 1,
                day   = 1,
            ).count()
        )


        # All posts for given month (January '2010)
        self.assertEquals(post_per_month,
            Post.objects.by_date(
                year  = year,
                month = 1
            ).count()
        )

        # All posts for given year
        self.assertEquals(post_per_month * month_number,
            Post.objects.by_date(
                year = year
            ).count()
        )

    #------------------------------------------------------------------------ #

    def testDatePublicFromCreate(self):
        """
        Tests that ``created_at`` filled by ``public_from`` value if
        it specified AND model just created (PK is NoneType)
        """
        self.post.save()
        #self.post.publish()
        self.assertEquals(self.post.public_from, self.post.created_at)


    def testPublicFromEmpty(self):
        """
        Tests built-in Post manager in case when ``public_from`` field is empty
        """
        self.post.save()
        #self.post.publish()
        self.assertEquals(1, Post.objects.count())


    def testPublicFromYesterday(self):
        """
        Tests built-in Post manager in case when ``public_from`` field is
        set to past date
        """
        self.post.public_from = self.day_yesterday
        self.post.save()
        #self.post.publish()
        self.assertEquals(1, Post.objects.count())

    def testPublicFromTomorrow(self):
        """
        Tests built-in Post manager in case when ``public_from`` field
        is set to future date
        """
        self.post.public_from = self.day_tomorrow
        self.post.save()
        #self.post.publish()
        self.assertEquals(0, Post.objects.count())

    # ----------------------------------------------------------------------- #

    def testPublicTillPast(self):
        """
        Tests built-in Post manager in case when ``public_till`` field
        is set to past date
        """
        self.post.public_till = self.day_yesterday
        self.post.public_from = self.post.public_till - timedelta(1)
        self.post.save()
        #self.post.publish()
        self.assertEquals(0, Post.objects.count())

    def testPublicTillFuture(self):
        """
        Tests built-in Post manager in case when ``public_from`` field
        is set to future date
        """
        self.post.public_till = self.day_tomorrow
        self.post.save()
        #self.post.publish()
        self.assertEquals(1, Post.objects.count())

    def testPublicTillLessThanPublicFrom(self):
        """
        Tests built-in Post manager in case when ``public_till`` field
        is less than ``public_from`` set to future date
        """
        def error():
            self.post.public_till = self.day_yesterday
            self.post.public_from = self.day_tomorrow
            self.post.save()

        self.assertRaises(exceptions.ValidationError, error)

    def testBothPublicFieldFound(self):
        """
        Tests built-in Post manager in case when both ``public_from``
        and ``public_till`` field  is set and ``public_from`` is less
        than ``public_till``
        """
        self.post.public_till = self.day_tomorrow
        self.post.public_from = self.day_yesterday
        self.post.save()
        #self.post.publish()
        self.assertEquals(1, Post.objects.count())

    # ----------------------------------------------------------------------- #

    def testIsActiveOn(self):
        self.post.is_active=True
        self.post.save()
        #self.post.publish()
        self.assertEquals(1, Post.objects.count())

    def testIsActiveOff(self):
        self.post.is_active=False
        self.post.save()
        #self.post.publish()
        self.assertEquals(0, Post.objects.count())

    # ----------------------------------------------------------------------- #

    def testInstance(self):
        """
        Tests that Post is child of PeriodicsBase and Publisher classes
        """
        self.assertTrue(isinstance(self.post, PeriodicsBase))
        self.assertTrue(isinstance(self.post, Publisher))

    # ----------------------------------------------------------------------- #

    def testEmptyTitle(self):
        def error():
            self.post.title = ''
            self.post.save()
        self.assertRaises(exceptions.ValidationError, error)

    # ----------------------------------------------------------------------- #

    def testEmptySlug(self):
        def error():
            self.post.slug = ''
            self.post.save()
        self.assertRaises(exceptions.ValidationError, error)

    # ----------------------------------------------------------------------- #

    def testPictureNotExistsAndOff(self):
        """
        Tests that ``picture`` property returns None when ``picture_src``
        field is *NOT* filled and ``picture_show`` is off
        """
        self.post.picture_src = None
        self.post.picture_show = False
        self.post.save()
        self.assertFalse(self.post.picture is not None)


    def testPictureExistsAndOff(self):
        """
        Tests that ``picture`` property returns None when ``picture_src``
        field is filled and ``picture_show`` is off
        """
        self.post.picture_src = 'foo.gif'
        self.post.picture_show = False
        self.post.save()
        self.assertFalse(self.post.picture is not None)

    def testPictureExistsAndOn(self):
        """
        Tests that ``picture`` property returns ImageField object
        if ``picture_src`` is not empty and ``picture_show`` is ON
        """
        self.post.picture_src = 'foo.gif'
        self.post.picture_show = True
        self.post.save()
        self.assertFalse(self.post.picture is None) # TODO isinstance + ImageField

    # ----------------------------------------------------------------------- #

class UpdatePostTest(TestCase):
    def setUp(self):
        """
        Prepare test environment
        """

        # Post instance template (must be filled correctly)
        self.post = Post(
            title = 'Lorem ipsum',
            slug  = 'lorem-ipsum',
        )
        
        self.url = urlresolvers.reverse('post-save')
        self.client = client.Client()

        user = set_up_user()
        user.is_active = True
        user.is_staff  = True
        user.save()

        self.client.login(
            username = user.username,
            password = 'test',
        )

    def testViewIsExists(self):
        response = self.client.get(self.url)
        self.assertNotEquals(404, response.status_code)  

    def testViewAdminUser(self):
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)    

    def testViewAnonymousUser(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEquals(403, response.status_code)
