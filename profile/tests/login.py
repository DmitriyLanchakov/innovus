# encoding: utf-8
from django.test import TestCase, client
from django.contrib.auth.models import User


class LoginTest(TestCase):

    def setUp(self):
        self.password = User.objects.make_random_password()
        self.client = client.Client()

    def test_login_length(self):
        user = User.objects.create_user(
                username='verylongloginnamefortestlengthvalidationinloginform', 
                email='test@test.te', 
                password=self.password)
        data = {'username': user.username, 'password': self.password}
        response = self.client.post(reverse('profile_login'), data)
        print response

