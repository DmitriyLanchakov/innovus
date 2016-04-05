# -*- coding: utf-8 -*-

from django.test import TestCase, client
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth.models import User
from profile.forms import *
from django.contrib.localflavor import cl
from profile.tests import get_full_valid_data
from profile import CLAIM_WAITING_APPROVEMENT

class DelegateTest(TestCase):
    def get_delegate_data(self):
        data = get_full_valid_data()
        data['is_take_part'] = str(TAKE_PART_DELEGATE)

        drop = [
            'phone', 'phone_extra', 'address', 'fax', 'skype', 'icq',
            'site', 'blog', 'twitter', 'email', 'password', 'confirm',
        ]

        for d in drop:
            data.pop(d)
        return data

class DelegateFormTest(DelegateTest):
    def test_validate_form_with_context_delegate(self):
        form = ClaimForm(self.get_delegate_data())
        self.assertTrue(form.is_valid())


    def test_validate_form_with_context_delegate_no_geo(self):
        data = self.get_delegate_data()
        del data['country']
        form = ClaimForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue('country' in form._errors)

    def test_validate_form_with_context_delegate_no_charter(self):
        data = self.get_delegate_data()
        del data['arrival_want_charter']
        del data['departure_want_charter']

        form = ClaimForm(data)

        self.assertFalse(form.is_valid())
        self.assertTrue('arrival_want_charter' in form._errors)
        self.assertTrue('departure_want_charter' in form._errors)

# --------------------------------------------------------------------------- #

class DelegateViewTest(DelegateTest):
    def setUp(self):
        self.delegate_url = reverse('add_delegate')
        self.registration_url = reverse('join_participant')
        self.client = client.Client()

        # Create contact
        data = get_full_valid_data()
        self.client.post(self.registration_url, data)

        # Activate contact
        self.contact = User.objects.get(pk=1)
        self.contact.is_active=True
        self.contact.save()

        # Authenticate contact
        self.client.login(
            username = data['email'],
            password = data['password'],
        )

    def test_validate_view_(self):
        self.assertEquals(1, Claim.objects.count())

        self.client.post(self.delegate_url, self.get_delegate_data())

        self.assertEquals(2, Claim.objects.count())
        self.assertEquals(1, Claim.objects.filter(delegation_manager=self.contact).count())
        self.assertEquals(1, Claim.objects.filter(delegation_manager=None).count())

        claim = Claim.objects.order_by('-id')[0]

        self.assertNotEquals(None, claim.room_category)
        self.assertEquals(CLAIM_WAITING_APPROVEMENT, claim.claim_state)

    def test_edit_delegate_integro(self):
        # Create delegate
        data = self.get_delegate_data()

        # Create delegate
        self.client.post(self.delegate_url, data)

        # Retrieve delegate object
        self.assertEquals(2, Claim.objects.count())
        claims  = Claim.objects.order_by('id')
        contact, delegate = claims[0], claims[1]

        # Go on edit delegate view
        url = reverse('edit_delegate', kwargs=dict(id=delegate.pk))

        resp = self.client.get(url)

        # Update delegate
        data['first_name'] = 'Steve'
        data['last_name'] = 'Ballmer'

        resp = self.client.post(url, data)

        self.assertEquals(302, resp.status_code)


        # Retrieve delegate object and check no new entites created
        delegate = Claim.objects.order_by('-id')[0]
        self.assertEquals(2, Claim.objects.count())
        self.assertEquals(contact, delegate.delegation_manager)

        self.assertEquals('Steve', delegate.first_name)
        self.assertEquals('Ballmer', delegate.last_name)

    def test_delete_delegate_integro(self):
        # Create delegate
        data = self.get_delegate_data()

        # Create delegate
        self.client.post(self.delegate_url, data)

        # Retrieve delegate object
        self.assertEquals(2, Claim.objects.count())
        delegate = Claim.objects.order_by('-id')[0]

        # Go on edit delegate view
        url = reverse('delete_delegate', kwargs=dict(id=delegate.pk))
        resp = self.client.get(url)

        self.client.post(url, data)

        # Retrieve delegate object and check no new entites created
        self.assertEquals(2, Claim.objects.count())
        self.assertEquals(1, Claim.objects.filter(is_deleted=True).count())
        self.assertEquals(0, Claim.objects.filter(is_deleted=False,delegation_manager=self.contact).count())

