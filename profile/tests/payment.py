# -*- coding: utf-8 -*-

from datetime import datetime, date
from django.test import TestCase, client as test_client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core import mail
from profile.exceptions import IncorrectClaimStateException
from profile.tests import get_full_valid_data
from profile.forms import ClaimForm
from profile import CLAIM_WAITING_PAYMENT, CLAIM_ACCEPTED, CLAIM_CANCELLED, \
    CLAIM_REJECTED, CLAIM_SENT, CLAIM_WAITING_APPROVEMENT
from profile.models import Claim

class PaymentTest(TestCase):
    def setUp(self):
        self.claim = ClaimForm(get_full_valid_data()).save()
        self.claim.claim_state = CLAIM_WAITING_PAYMENT
        self.money = 10000
        self.date  = date.today()

    def get_claim(self):
        return Claim.objects.get(pk=1)

    def test_payment_success(self):
        self.claim.payment(self.money, self.date)
        self.assertEquals(CLAIM_ACCEPTED,   self.get_claim().claim_state)
        self.assertAlmostEquals(self.money, self.get_claim().payment_sum)

    def test_is_waiting_payment_after(self):
        self.claim.payment(self.money, self.date)
        self.assertFalse(self.get_claim().is_waiting_payment())

    def test_is_waiting_payment(self):
        self.claim.claim_state = CLAIM_WAITING_PAYMENT
        self.claim.save()
        self.assertTrue(self.get_claim().is_waiting_payment())

    def test_payment_fail_if_initial_status_is_not_waiting_payment(self):
        wrong_states = [
            CLAIM_ACCEPTED,  CLAIM_CANCELLED,   CLAIM_REJECTED,
            CLAIM_SENT,      CLAIM_WAITING_APPROVEMENT
        ]

        for state in wrong_states:
            def catch_exception():
                self.claim.claim_state = state
                self.claim.save()
                self.claim.payment(self.money, self.date )

            self.assertRaises(IncorrectClaimStateException, catch_exception)

    def test_payment_success_if_not_waiting_payment_and_paid(self):
        wrong_states = [
            CLAIM_ACCEPTED,  CLAIM_CANCELLED,   CLAIM_REJECTED,
            CLAIM_SENT,      CLAIM_WAITING_APPROVEMENT
        ]

        for state in wrong_states:
            self.claim.claim_state = state
            self.claim.payment_date = datetime.now()
            self.claim.save()
            self.claim.payment(self.money, self.date )

    def test_payment_view_redirect_to_login_if_not_admin(self):
        User.objects.create_user('demo', 'demo@demo.de', 'demo')

        client = test_client.Client()
        client.login(username='demo', password='demo')

        # Построить подопытный URL
        url = reverse('manage_claim_payment', kwargs=dict(id = self.claim.id))

        # Перейти на страницу оплаты. убедиться. что она есть
        resp = client.get(url)
        self.assertEqual(302, resp.status_code)

    def test_payment_view_redirect_to_login_if_unauth(self):
        url = reverse('manage_claim_payment', kwargs=dict(id = self.claim.id))
        client = test_client.Client()
        resp = client.get(url)
        self.assertEqual(302, resp.status_code)

    def test_payment_view_404_if_not_waiting(self):
        User.objects.create_superuser('demo', 'demo@demo.de', 'demo')
        client = test_client.Client()
        client.login(username='demo', password='demo')
        url = reverse('manage_claim_payment', kwargs=dict(id=self.claim.id))
        resp = client.get(url)
        self.assertEqual(404, resp.status_code)

    def test_payment_view_404_if_paid(self):
        User.objects.create_superuser('demo', 'demo@demo.de', 'demo')
        client = test_client.Client()
        client.login(username='demo', password='demo')
        url = reverse('manage_claim_payment', kwargs=dict(id=self.claim.id))

        self.claim.claim_state = CLAIM_SENT
        self.claim.bill_date = None
        self.claim.save()

        resp = client.get(url)
        self.assertEqual(404, resp.status_code)


    def test_payment_view_200_if_paid_or_waiting(self):
        User.objects.create_superuser('demo', 'demo@demo.de', 'demo')
        client = test_client.Client()
        client.login(username='demo', password='demo')
        url = reverse('manage_claim_payment', kwargs=dict(id=self.claim.id))

        self.claim.claim_state = CLAIM_WAITING_PAYMENT
        self.claim.bill_date = datetime.now()
        self.claim.save()

        resp = client.get(url)
        self.assertEqual(200, resp.status_code)


    def test_payment_view_integro(self):
        # Создать суперпользователя
        User.objects.create_superuser('demo', 'demo@demo.de', 'demo')

        client = test_client.Client()
        client.login(username='demo', password='demo')


        # Пометить заявку как ожидающую оплаты
        self.claim.claim_state = CLAIM_WAITING_PAYMENT
        self.claim.save()

        # Построить подопытный URL
        url = reverse('manage_claim_payment', kwargs=dict(id = self.claim.id))

        # Перейти на страницу оплаты. убедиться. что она есть
        resp = client.get(url)
        self.assertEqual(200, resp.status_code)

        # Заполнить форму оплаты
        resp = client.post(url, dict(sum=10000, date='07.05.2010'))

        # Проверить, что произошёл редирект (форма правильно заполнена)
        self.assertEquals(302, resp.status_code)

        # Проверить, что письмо c подстрокой 'claim successfully paid' в очереди
        from django.template.loader import render_to_string
        subject = render_to_string('profile/email/payment.subj.html')
        self.assertTrue(subject == mail.outbox[-1].subject)

        ## Проверить, что теперь страницы не существует
        resp = client.get(url)
        self.assertEquals(200, resp.status_code)

    #def test_payment_view_integro(self):

