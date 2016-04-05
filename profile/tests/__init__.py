# -*- coding: utf-8 -*-


from django.test import TestCase as DjangoTestCase, client
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth.models import User
from profile.forms import *
from django.contrib.localflavor import cl

# --------------------------------------------------------------------------- #

def get_full_valid_data():
    """
    Образцово-показательно заполненная форма
    """
    return {
        'first_name'    : 'William',
        'last_name'     : 'Henry',
        'middle_name'   : 'Gates',
        'gender'        : '1',
        'country'       : '170',
        'region'        : '77',   # Moscow region
        'city'          : '1125', # Moscow
        'citizenship'   : 'Russian Federation',

        'phone'         : '+7 (495) 1234567',
        'phone_extra'   : '+7 (495) 7654321',
        'address'       : '1, Red Square, Moscow, RU',
        'fax'           : '+7 (495) 7654321',
        'skype'         : 'ivanov',
        'icq'           : '77777',
        'site'          : 'http://microsoft.com',
        'blog'          : 'http://microsoft.com/bgates/',
        'twitter'       : 'http://twitter.com/billgates',

        'email'         : 'bill@hotmail.com',
        'password'      : 'p455w0rd',
        'confirm'       : 'p455w0rd',
        'industry'      : '3',
        'orgranization' : 'Microsoft LLC',
        'position'      : 'CEO',

        'arrival_want_charter'   : '0',
        'arrival_transport_type' : '4',
        'arrival_date'           : '2010-05-19 14:00:00',

        'departure_want_charter'   : '0',
        'departure_transport_type' : '4',
        'departure_date'           : '2010-05-21 14:00:00',

        'need_hotel'    : '1',
        'room_category' : '2',
        'is_take_part'  : '1',
    }

# --------------------------------------------------------------------------- #

class TestCase(DjangoTestCase):
    def browser(self, view, data):
        url  = reverse(view)
        self.client.get(url)
        return self.client.post(url, data)

# --------------------------------------------------------------------------- #

class RegistrationFormTest(TestCase):
    #fixtures = ['apps/profile/fixtures/test_initial_data.json']
#    fixtures = ['country_region_city.json', 'industries.json']

    def test_valid_form_is_success(self):
        form = ClaimForm(get_full_valid_data())
        self.assertTrue(form.is_valid())

    def test_clean_email_fail(self):
        User.objects.create(
            username = 'bill@hotmail.com',
            password = '123456',
            email    = 'bill@hotmail.com',
        )

        form = ClaimForm(get_full_valid_data())
        self.assertFalse(form.is_valid())
        self.assertTrue('email' in form._errors)

    def test_clean_email_success(self):
        users = User.objects.all()
        users.delete()

        form = ClaimForm(get_full_valid_data())
        self.assertTrue(form.is_valid())

    def test_clean_password_fail(self):
        failed_data = get_full_valid_data()
        failed_data['password'] = ''

        form = ClaimForm(failed_data)

        self.assertFalse(form.is_valid())
        self.assertTrue('password' in form._errors)

    def test_clean_password_success(self):
        success_data = get_full_valid_data()
        success_data['password'] = 'v3rystr0ngp455w0rd'
        success_data['email'] = 'wrong_email'

        form = ClaimForm(success_data)
        form.is_valid()

        self.assertTrue('password' not in form._errors)
        self.assertTrue('email' in form._errors)

    # ----------------------------- Confirm --------------------------------- #

    def test_clean_confirm_success(self):
        success_data = get_full_valid_data()
        success_data['password'] = 'v3rystr0ngp455w0rd'
        success_data['confirm']  = 'v3rystr0ngp455w0rd'
        success_data['email']    = 'wrong_email'

        form = ClaimForm(success_data)
        form.is_valid()

        self.assertTrue('confirm' not in form._errors)
        self.assertTrue('email' in form._errors)


    def test_clean_confirm_success_empty_filed(self):
        success_data = get_full_valid_data()
        success_data['confirm']  = ''

        form = ClaimForm(success_data)

        self.assertFalse(form.is_valid())
        self.assertTrue('confirm' in form._errors)

    def test_clean_confirm_success_does_not_match(self):
        success_data = get_full_valid_data()
        success_data['password'] = '123456'
        success_data['confirm']  = '654321'

        form = ClaimForm(success_data)

        self.assertFalse(form.is_valid())
        self.assertTrue('confirm' in form._errors)

    # ------------------------------- Country ------------------------------- #

    def test_clean_country(self):
        success_data = get_full_valid_data()
        success_data['country'] = ''

        form = ClaimForm(success_data)

        self.assertFalse(form.is_valid())
        self.assertTrue('country' in form._errors)

    # ------------------------------- Region -------------------------------- #

    def test_clean_region_empty_if_not_russia(self):
        data = get_full_valid_data()
        data['country'] = RUSSIA_COUNTRY_ID - 1
        data['region'] = ''
        data['city'] = ''

        form = ClaimForm(data)
        form.is_valid()

        self.assertTrue(form.is_valid())

    def test_clean_region_required_if_russia(self):
        data = get_full_valid_data()
        data['country'] = RUSSIA_COUNTRY_ID
        data['region'] = TOMSK_REGION_ID
        data['city'] = TOMSK_CITY_ID

        form = ClaimForm(data)
        self.assertTrue(form.is_valid())

    def test_clean_region_required_if_russia_empty(self):
        data = get_full_valid_data()
        data['country'] = RUSSIA_COUNTRY_ID
        data['region'] = ''

        form = ClaimForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue('region' in form._errors)

    # ---------------------- Want charters ---------------------------------- #

    def test_clean_arrival_want_charter(self):
        data = get_full_valid_data()
        data['arrival_want_charter'] = ''

        form = ClaimForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue('arrival_want_charter' in form._errors)

    def test_clean_departure_want_charter(self):
        data = get_full_valid_data()
        data['departure_want_charter'] = ''

        form = ClaimForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue('departure_want_charter' in form._errors)

    # --------------------- Arrival date ------------------------------------ #

    def test_arrival_date_without_charter_empty_value(self):
        data = get_full_valid_data()
        data['arrival_date'] = ''

        form = ClaimForm(data)

        self.assertFalse(form.is_valid())
        self.assertTrue('arrival_date' in form._errors)

    def test_arrival_date_with_want_charter(self):
        data = get_full_valid_data()
        data['arrival_date'] = ''
        data['arrival_transport_type'] = ''
        data['arrival_want_charter'] = '1'

        form = ClaimForm(data)
        self.assertTrue(form.is_valid())

    def test_arrival_date_with_want_charter_and_wrong_date(self):
        data = get_full_valid_data()
        data['arrival_date'] = 'wr0ng date'
        data['arrival_want_charter'] = '1'

        form = ClaimForm(data)
        self.assertTrue(form.is_valid())


    def test_arrival_date_without_charter_wrong_value(self):
        data = get_full_valid_data()
        data['arrival_date'] = 'wrong_date'

        form = ClaimForm(data)

        self.assertFalse(form.is_valid())
        self.assertTrue('arrival_date' in form._errors)

    # --------------------- Departure date ---------------------------------- #

    def test_departure_date_without_charter_empty_value(self):
        data = get_full_valid_data()
        data['departure_date'] = ''

        form = ClaimForm(data)

        self.assertFalse(form.is_valid())
        self.assertTrue('departure_date' in form._errors)

    def test_departure_date_with_want_charter(self):
        data = get_full_valid_data()
        data['departure_date'] = ''
        data['departure_want_charter'] = '1'

        form = ClaimForm(data)

        self.assertTrue(form.is_valid())

    def test_departure_date_with_want_charter_and_wrong_date(self):
        data = get_full_valid_data()
        data['departure_date'] = 'wr0ng date'
        data['departure_want_charter'] = '1'

        form = ClaimForm(data)
        self.assertTrue(form.is_valid())


    def test_departure_date_without_charter_wrong_value(self):
        data = get_full_valid_data()
        data['departure_date'] = 'wrong_date'

        form = ClaimForm(data)

        self.assertFalse(form.is_valid())
        self.assertTrue('departure_date' in form._errors)

    # --------------------- Arrival transport type -------------------------- #

    def test_arrival_transport_type_and_want_charter(self):
        data = get_full_valid_data()
        data['arrival_want_charter'] = '1'

        form = ClaimForm(data)

        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['arrival_transport_type'] is None)


    def test_arrival_transport_type_and_not_want_charter_not_filled(self):
        data = get_full_valid_data()
        data['arrival_transport_type'] = ''

        form = ClaimForm(data)

        self.assertFalse(form.is_valid())
        self.assertTrue('arrival_transport_type' in form._errors)


    def test_arrival_transport_type_and_not_want_charter_filled(self):
        data = get_full_valid_data()
        form = ClaimForm(data)
        self.assertTrue(form.is_valid())

    # --------------------- Deprture transport type ------------------------- #

    def test_departure_transport_type_and_want_charter_not_filled(self):
        data = get_full_valid_data()
        data['departure_want_charter'] = '1'

        form = ClaimForm(data)

        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['departure_transport_type'] is None)

    def test_departure_transport_type_and_want_charter_filled(self):
        data = get_full_valid_data()
        data['departure_want_charter'] = '1'
        data['departure_transport_type'] = '2'
        form = ClaimForm(data)

        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['departure_transport_type'] is None)

    def test_departure_transport_type_and_not_want_charter_not_filled(self):
        data = get_full_valid_data()
        data['departure_transport_type'] = ''

        form = ClaimForm(data)

        self.assertFalse(form.is_valid())
        self.assertTrue('departure_transport_type' in form._errors)


    def test_departure_transport_type_and_not_want_charter_filled(self):
        data = get_full_valid_data()
        form = ClaimForm(data)
        self.assertTrue(form.is_valid())

    # -------------------- Need hotel and room category ---------------------- #

    def test_clean_room_category_when_need_hotel_success(self):
        self.assertTrue(ClaimForm(get_full_valid_data()).is_valid())

    def test_clean_room_category_when_not_filled_and_hotel_needed(self):
        data = get_full_valid_data()
        data['room_category'] = ''

        form = ClaimForm(data)

        self.assertFalse(form.is_valid())
        self.assertTrue('room_category' in form._errors)

    def test_clean_room_category_when_no_need_hotel_not_filled(self):
        data = get_full_valid_data()
        data['room_category'] = ''
        data['need_hotel'] = '0'

        form = ClaimForm(data)

        self.assertTrue(form.is_valid())
        self.assertEquals(0, form.cleaned_data['room_category'])

    def test_clean_room_category_when_no_need_hotel_and_category_filled(self):
        data = get_full_valid_data()
        data['room_category'] = '1'
        data['need_hotel'] = '0'

        form = ClaimForm(data)

        self.assertTrue(form.is_valid())
        self.assertEquals(0, form.cleaned_data['room_category'])

    # ----------------------------------------------------------------------- #

    def travel_clean_helper(self, field_name, field_value, expected=None):
        data = get_full_valid_data()
        data[field_name] = field_value

        data['country'] = str(RUSSIA_COUNTRY_ID)
        data['region']  = str(TOMSK_REGION_ID)
        data['city']    = str(TOMSK_CITY_ID)

        form = ClaimForm(data)

        self.assertTrue(form.is_valid())
        self.assertEquals(expected, form.cleaned_data[field_name])

    def test_travel_departure_date(self):
        self.travel_clean_helper('departure_date', '23.05.2010 12:34')

    def test_travel_departure_transport_type(self):
        self.travel_clean_helper('departure_transport_type', '4')

    def test_travel_departure_want_charter(self):
        self.travel_clean_helper('departure_want_charter', '1', 0)


    def test_travel_arrival_date(self):
        self.travel_clean_helper('arrival_date', '19.05.2010 12:34')

    def test_travel_arrival_transport_type(self):
        self.travel_clean_helper('arrival_transport_type', '4')

    def test_travel_arrival_want_charter(self):
        self.travel_clean_helper('arrival_want_charter', '1', 0)

    def test_travel_need_hotel(self):
        self.travel_clean_helper('need_hotel', '1')

    def test_travel_room_category(self):
        self.travel_clean_helper('room_category', '1', 0)

    # ---------------------------- take_part -------------------------------- #

    def test_clean_take_part_dont_wont(self):
        data = get_full_valid_data()
        data['is_take_part'] = str(TAKE_PART_CONTACT_WO_P)

        form = ClaimForm(data)
        self.assertTrue(form.is_valid())
        self.assertEquals(None, form.cleaned_data['arrival_date'])
        self.assertEquals(None, form.cleaned_data['arrival_transport_type'])
        self.assertEquals(0, form.cleaned_data['arrival_want_charter'])

        self.assertEquals(None, form.cleaned_data['departure_date'])
        self.assertEquals(None, form.cleaned_data['departure_transport_type'])
        self.assertEquals(0, form.cleaned_data['departure_want_charter'])

        self.assertEquals(0, form.cleaned_data['room_category'])

    def test_clean_take_part_want(self):
        data = get_full_valid_data()

        data['is_take_part'] = '1'
        data['arrival_date'] = '2012-12-21 12:12:12'
        data['arrival_transport_type'] = '3'
        data['arrival_want_charter'] = '0'
        data['departure_date']  = '2012-12-21 12:12:12'
        data['departure_transport_type'] = '2'
        data['departure_want_charter'] = '1'
        data['room_category'] = '3'
        data['need_hotel'] = '1'

        form = ClaimForm(data)

        self.assertTrue(form.is_valid())
        self.assertEquals(True, isinstance(form.cleaned_data['arrival_date'], datetime))
        self.assertEquals(3, form.cleaned_data['arrival_transport_type'])
        self.assertEquals(0, form.cleaned_data['arrival_want_charter'])

        self.assertEquals(None, form.cleaned_data['departure_date'])
        self.assertEquals(None, form.cleaned_data['departure_transport_type'])
        self.assertEquals(1, form.cleaned_data['departure_want_charter'])

        self.assertEquals(3, form.cleaned_data['room_category'])

    def test_claim_type(self):
        data = get_full_valid_data()
        form = ClaimForm(data)

        self.assertTrue(form.is_valid())
        
        model = form.save()
        from profile.models import CLAIM_TYPE_PART
        self.assertEquals(CLAIM_TYPE_PART, model.claim_type)
        
# --------------------------------------------------------------------------- #

class RegistrationViewTest(TestCase):
#    fixtures = ['country_region_city.json', 'industries.json']

    def setUp(self):
        self.url = reverse('join_participant')
        self.client = client.Client()

    def test_view_exists(self):
        resp = self.client.get(self.url)
        self.assertEquals(200, resp.status_code)


    def test_view_registration_success(self):
        """
        Эмулирует полное (валидное) заполнение формы и отправку её
        на сервер. При этом должен создаться пользователь

        """

        # Убедились, что у нас нет ни одного пользоателя
        self.assertEquals(0, User.objects.count())

        # Make request
        data = get_full_valid_data()
        resp = self.client.post(self.url, data)

        # Сервер не сломался, пользоатель появился, а его email совпадает с
        # введённым
        self.assertEquals(302, resp.status_code)
        self.assertEquals(1, User.objects.count())
        self.assertEquals(data['email'], User.objects.get(pk=1).email)
        self.assertEquals(CLAIM_TYPE_PART, User.objects.get(pk=1).get_profile().claim_type)

        """
        self.assertEquals(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEquals(mail.outbox[0].subject, 'Subject here')

        """
        # Verify that the subject of the first message is correct.
        #self.assertEquals(mail.outbox[0].subject, 'Subject here')

    def test_need_hotel_is_true(self):
        self.client.post(self.url, get_full_valid_data())
        claim = User.objects.get(pk=1).get_profile()
        self.assertNotEquals(None, claim.room_category)

    def test_need_hotel_is_false(self):
        data = get_full_valid_data()
        data['need_hotel'] = '0'

        self.client.post(self.url, data)
        claim = User.objects.get(pk=1).get_profile()
        self.assertTrue(claim.room_category is 0)

    def test_is_take_part_empty(self):
        data = get_full_valid_data()
        del data['is_take_part']

        resp = self.client.post(self.url, data)

        self.assertEquals(200, resp.status_code)
        self.assertTrue('is_take_part' in resp.context['claim_form']._errors)

    def test_is_take_part_wrong(self):
        data = get_full_valid_data()
        data['is_take_part'] = 'abcdefghijklmnopqrstuvwxyz'

        resp = self.client.post(self.url, data)

        self.assertEquals(200, resp.status_code)
        self.assertTrue('is_take_part' in resp.context['claim_form']._errors)

# --------------------------------------------------------------------------- #

class EditFormTest(TestCase):
    fixtures = ['apps/profile/fixtures/claims.json',]

    def setUp(self):
        self.claim = Claim.objects.all()[0]


    def test_email_empty(self):
        data = get_full_valid_data()
        data['email'] = ''
        form = ClaimForm(data, instance=self.claim)

        self.assertTrue(form.is_valid())
        self.assertEquals(self.claim.email, form.cleaned_data['email'])


    def test_password_empty(self):
        data = get_full_valid_data()
        data['password'] = ''
        form = ClaimForm(data, instance=self.claim)

        self.assertTrue(form.is_valid())
        self.assertEquals(None, form.cleaned_data['password'])


    def test_confirm_empty(self):
        data = get_full_valid_data()
        data['confirm'] = ''
        form = ClaimForm(data, instance=self.claim)

        self.assertTrue(form.is_valid())
        self.assertEquals(None, form.cleaned_data['confirm'])

    def test_email_edit(self):
        data = get_full_valid_data()
        data['email'] = 'wr0ng d4t4'
        form = ClaimForm(data, instance=self.claim)

        self.assertTrue(form.is_valid())
        self.assertEquals(self.claim.email, form.cleaned_data['email'])


    def test_password_edit(self):
        data = get_full_valid_data()
        data['password'] = ''
        form = ClaimForm(data, instance=self.claim)

        self.assertTrue(form.is_valid())
        self.assertEquals(None, form.cleaned_data['password'])


    def test_confirm(self):
        data = get_full_valid_data()
        data['confirm'] = ''
        form = ClaimForm(data, instance=self.claim)

        self.assertTrue(form.is_valid())
        self.assertEquals(None, form.cleaned_data['confirm'])

# --------------------------------------------------------------------------- #

class EditProfileViewTest(TestCase):

    def setUp(self):
        self.url = reverse('edit_participant')
        self.client = client.Client()

        # Registering new user
        data = get_full_valid_data()
        resp = self.client.post(reverse('join_participant'), data)

        # Activating user just created
        self.user = User.objects.get(pk=1)
        self.user.is_active = True
        self.user.save()

        # Authenticates
        self.client.login(
            username = data['email'],
            password = data['password']
        )

    def get_claim(self):
        return User.objects.get(pk=1).get_profile()

    def test_cancel_hotel_choice(self):
        self.assertEquals(2, self.user.get_profile().room_category)

        # We don't want hotel
        data = get_full_valid_data()
        data['need_hotel'] = '0'

        resp = self.client.post(self.url, data)

        self.assertEquals(302, resp.status_code)
        self.assertEquals(0, self.get_claim().room_category)

    def test_change_country_from_russia(self):
        data = get_full_valid_data()
        data['country'] = str(RUSSIA_COUNTRY_ID - 1)

        resp = self.client.post(self.url, data)

        self.assertEquals(302, resp.status_code)
        self.assertEquals(RUSSIA_COUNTRY_ID-1, self.get_claim().country.pk)
        self.assertEquals(None, self.get_claim().region)
        self.assertEquals(None, self.get_claim().city)


    def test_change_country_to_russia_without_region(self):
        data = get_full_valid_data()
        data['country'] = str(RUSSIA_COUNTRY_ID - 1)
        resp = self.client.post(self.url, data)


        data['country'] = str(RUSSIA_COUNTRY_ID)
        data['region']=''
        data['city']=''
        resp = self.client.post(self.url, data)


        self.assertEquals(200, resp.status_code)
        form = resp.context['claim_form']

        self.assertFalse(form.is_valid())
        self.assertTrue('region' in form._errors)
        self.assertEquals(1, len(form._errors))


    def test_change_country_to_russia_with_region_and_without_city(self):
        data = get_full_valid_data()
        data['country'] = str(RUSSIA_COUNTRY_ID - 1)
        resp = self.client.post(self.url, data)


        data['country'] = str(RUSSIA_COUNTRY_ID)
        data['region']  =  str(TOMSK_REGION_ID)
        data['city']    = ''
        resp = self.client.post(self.url, data)


        self.assertEquals(200, resp.status_code)
        form = resp.context['claim_form']

        self.assertFalse(form.is_valid())
        self.assertTrue('city' in form._errors)
        self.assertEquals(1, len(form._errors))

    def test_change_country_to_russia_with_region_and_city(self):
        data = get_full_valid_data()
        data['country'] = str(RUSSIA_COUNTRY_ID - 1)
        resp = self.client.post(self.url, data)

        data['country'] = str(RUSSIA_COUNTRY_ID)
        data['region'] = str(TOMSK_REGION_ID)
        data['city'] = str(TOMSK_CITY_ID)

        resp = self.client.post(self.url, data)

        self.assertEquals(302, resp.status_code)
        self.assertEquals(RUSSIA_COUNTRY_ID, self.get_claim().country.pk)
        self.assertEquals(TOMSK_REGION_ID,   self.get_claim().region.pk)
        self.assertEquals(TOMSK_CITY_ID,     self.get_claim().city.pk)

    def test_cancel_claim_integro(self):
        url = reverse('cancel_claim')
        self.client.get(url)

        resp = self.client.post(url)
        claim = self.get_claim()

        self.assertEquals(302, resp.status_code)
        self.assertTrue(claim.claim_state)

# --------------------------------------------------------------------------- #
from profile.tests.actions import *
from profile.tests.changes import *
from profile.tests.contacter_wo import *
from profile.tests.contacter_w import *
from profile.tests.converter import *
from profile.tests.delegate import *
from profile.tests.delivery import *
from profile.tests.payment import *
from profile.tests.reserv import *

