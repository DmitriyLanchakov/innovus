# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from annoying.functions import get_object_or_None

from .models import Region, City, Claim, Hotel, HotelRoomCategory
from profile.utils import get_hotel_choices
from .utils import get_countries, get_regions, get_industries
from profile import filters
import profile.settings as profile_settings


HOTEL_CHOICES = (
    (None, _('---------')),
    (0, _('no')),
    (1, _('yes')),
)
PROGRAMM_CHOICES = (
    (None, _('---------')),
) + profile_settings.PROGRAMM_TYPE_CHOICES


class ActionForm(forms.Form):
    action_code = forms.IntegerField(widget=forms.HiddenInput)


class ClaimForm(forms.ModelForm):
#    need_hotel  = forms.ChoiceField(widget=forms.Select,
#    choices=HOTEL_CHOICES,  required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False,
                label=_('Set the password to be used for login to INNOVUS'))
    confirm = forms.CharField(widget=forms.PasswordInput, required=False,
                        label=_('Enter the password again'))
    arrival_date = forms.DateTimeField(localize=True)
    departure_date = forms.DateTimeField(localize=True)
    programm_type = forms.ChoiceField(choices=PROGRAMM_CHOICES,
            label=_('programm type'))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.context = kwargs.pop('context', None)

        super(ClaimForm, self).__init__(*args, **kwargs)

        self._setup_geo()
#        self._move_need_hotel()
#        self._populate_need_hotel()

#    def _move_need_hotel(self):
#        """
#        Перемещает поле need_hotel в форме перед полем 'room_category'
#        """
#        index = self.fields.keyOrder.index('need_hotel')
#        self.fields.keyOrder.pop(index)
#        self.fields.keyOrder.insert(
#            self.fields.keyOrder.index('room_category')-1,
#            'need_hotel'
#        )

#    def _populate_need_hotel(self):
#        """
#        Заполняет не присутствующее в модели поле 'need_hotel' в случае,
#        когда пользователь редактирует заявку на участие или делегата
#        """
#        if self.instance.pk is not None:
#            self.fields['need_hotel'].initial = '1' if \
#            self.instance.room_category else '0'

    def _setup_geo(self):
        country, region = 0, 0

        if self.instance.id is not None:
            pre_country = self.data.get('country')
            pre_region = self.data.get('region')
            if pre_country is None and self.instance.country is not None:
                country = getattr(self.instance.country, 'id')
            elif pre_country is not None and len(pre_country) > 0:
                country = int(pre_country)

            if pre_region is None and self.instance.region is not None:
                region = getattr(self.instance.region, 'id')
            elif pre_region is not None and len(pre_region) > 0:
                region = int(pre_region)

        # Works for registration
        else:
            if (hasattr(self.instance, 'country') and
                    self.instance.country is not None):
                country = self.instance.country.pk
            if (hasattr(self.instance, 'region') and
                    self.instance.region is not None):
                region = self.instance.region.pk

            pre_country = self.data.get('country')
            if pre_country:
                country = int(pre_country)
            pre_region = self.data.get('region')
            if pre_region:
                region = int(pre_region)
        # obs
        self.fields['region'].queryset = Region.objects.filter(
            country__exact = country,
        )

        self.fields['city'].queryset = City.objects.filter(
            country__pk = country,
            region__pk  = region,
        )


    def clean_email(self):
        is_take_part = self.cleaned_data.get('is_take_part')
        if is_take_part == profile_settings.TAKE_PART_DELEGATE:
            return None

        if self.instance.pk is not None:
            return self.instance.email

        email = self.cleaned_data.get('email')

        if not email:
            raise forms.ValidationError(
                _('You must provide your email address')
            )

        if email and get_object_or_None(User, username=email):
            raise forms.ValidationError(
                _('User with %(email)s already exists' % dict(email=email))
            )

        return email

    def clean_password(self):
        is_take_part = self.cleaned_data.get('is_take_part')
        if is_take_part == profile_settings.TAKE_PART_DELEGATE:
            return None
        if self.instance.pk is not None:
            return None
        if not self.cleaned_data.get('password', None):
            raise forms.ValidationError(_('You should provide some strong password for registering'))

        return self.cleaned_data.get('password')


    def clean_confirm(self):
        is_take_part = self.cleaned_data.get('is_take_part')
        if is_take_part == profile_settings.TAKE_PART_DELEGATE:
            return None
        if self.instance.pk is not None:
            return None
        confirmation = self.cleaned_data.get('confirm', None)

        if not confirmation:
            raise forms.ValidationError(_('You should provide password confirmation for registering'))

        if confirmation != self.cleaned_data.get('password', None):
            raise forms.ValidationError(_('Password does not match confirmation'))

        return confirmation


    def clean_phone(self):
        is_take_part = self.cleaned_data.get('is_take_part')
        if is_take_part == profile_settings.TAKE_PART_DELEGATE:
            return None

        if not self.cleaned_data.get('phone', None):
            raise forms.ValidationError(
                _('Please specify your phone number')
            )

        return self.cleaned_data.get('phone')

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if not country:
            raise forms.ValidationError(_('You did not provide your country name'))
        return country

    def clean_region(self):
        region = self.cleaned_data.get('region')
        country = self.cleaned_data.get('country')

        if not region:
            if country and country.pk == profile_settings.RUSSIA_COUNTRY_ID:
                raise forms.ValidationError(
                    _('Please specify a region of Russian Federation')
                )
        return region

    def clean_city(self):
        city = self.cleaned_data.get('city')
        region = self.cleaned_data.get('region')
        country = self.cleaned_data.get('country')

        if city is None:
            if (country is not None and region is not None and
                    country.pk == profile_settings.RUSSIA_COUNTRY_ID and
                    region.country == country):
                raise forms.ValidationError(
                    _('Please specify a city of Russian Federation'))
        return city

    def clean_programm_type(self):
        programm_type = self.cleaned_data.get('programm_type')
        if (programm_type is None or 
            programm_type not in [profile_settings.PROGRAMM_TYPE_YOUTH,
                profile_settings.PROGRAMM_TYPE_GENERAL]):
            raise forms.ValidationError(_('Please specify forum programm type'))
        return programm_type
# ---------------------------------------------------------- arrival/departure

    def clean_arrival_want_charter(self):
        return self._want_charter('arrival')

    def clean_departure_want_charter(self):
        return self._want_charter('departure')

    def clean_arrival_charter_date(self):
        arrival_want_charter = self.cleaned_data.get('arrival_want_charter')
        arrival_charter_date = self.cleaned_data.get('arrival_charter_date')
        if arrival_want_charter and not arrival_charter_date:
            raise forms.ValidationError(_("""Please, select available
                arrival charter date"""))
        return arrival_charter_date

    def clean_departure_charter_date(self):
        departure_want_charter = self.cleaned_data.get('departure_want_charter', None)
        departure_charter_date = self.cleaned_data.get('departure_charter_date', None)
        if departure_want_charter and not departure_charter_date:
            raise forms.ValidationError(_('Please, select available departure charter date'))
        return departure_charter_date

    def clean_arrival_transport_type(self):
        return self._transport_type('arrival')
    # Departure info

    def clean_departure_transport_type(self):
        return self._transport_type('departure')


    def clean_arrival_date(self):
        return self._date('arrival')
#
#
    def clean_departure_date(self):
        return self._date('departure')

## -----------------------------------------------------------
#    def clean_need_hotel(self):
#        try:
#            return int(self.cleaned_data['need_hotel'])
#        except ValueError:
#            raise forms.ValidationError(
#                _('Wrong value for need hotel')
#            )
#
#    def clean_room_category(self):
#        need = self.cleaned_data.get('need_hotel')
#        room = self.cleaned_data.get('room_category')
#
#        if not need:
#            return 0
#
#        if not room:
#            raise forms.ValidationError(_('we need to know a hotel room class'))
#
#        return self.cleaned_data['room_category']
## -------------------------------------------------------- generics

    def _want_charter(self, direction):
        want_charter = self.cleaned_data.get('%s_want_charter' % direction)

        if want_charter is None or (isinstance(want_charter, basestring) and len(want_charter) == 0):
            raise forms.ValidationError(
                _('Please specify want you to use charter')
            )
        return want_charter

    def _date(self, direction):
        want = self.cleaned_data.get('%s_want_charter' % direction)

        if want:
            return None

        date = self.cleaned_data['%s_date' % direction]

        if not date:
            raise forms.ValidationError(_('%(direction)s date is not set' % {'direction': direction }))

        return self.cleaned_data['%s_date' % direction]


    def _transport_type(self, direction):
        want = self.cleaned_data.get('%s_want_charter' % direction)

        if want:
            return None

        transport_type = self.cleaned_data['%s_transport_type' % direction]

        if not transport_type:
            raise forms.ValidationError(_('%(direction)s transport type is not set' % {'direction': direction }))

        return self.cleaned_data['%s_transport_type' % direction]


    def clean_is_take_part(self):
        take_part = self.cleaned_data.get('is_take_part')

        if take_part is None or (isinstance(take_part, basestring) and len(take_part)==0):
            raise forms.ValidationError(
                _('Please specify if want you to take part in the Forum')
            )
        return take_part

    def clean_claim_type(self):
        if not self.instance.pk:
            return profile_settings.CLAIM_TYPE_PART

        return self.cleaned_data.get('claim_type', profile_settings.CLAIM_TYPE_PART)


    def clean(self):
        self.cleaned_data = super(ClaimForm, self).clean()
        take_part = self.cleaned_data.get('is_take_part')

        country = self.cleaned_data.get('country')
        region  = self.cleaned_data.get('region')

        if country and country.id != profile_settings.RUSSIA_COUNTRY_ID:
            self.cleaned_data['region'] = None
            self.cleaned_data['city'] = None
            self._errors.pop('region', None)
            self._errors.pop('city', None)

        if take_part == profile_settings.TAKE_PART_CONTACT_WO_P or region and region.id == profile_settings.TOMSK_REGION_ID:
            cleaned_fields = [
                'departure_date', 'departure_transport_type',
                'departure_want_charter', 'arrival_date',
                'arrival_transport_type', 'arrival_want_charter',
            ]

            for cf in cleaned_fields:
                self.cleaned_data[cf] = None
                self._errors.pop(cf, None)

            self.cleaned_data['arrival_want_charter'] = 0
            self.cleaned_data['departure_want_charter'] = 0
#            self.cleaned_data['room_category']=0

        for direction in ['arrival', 'departure']:
            if self.cleaned_data.get('%s_want_charter' % direction):
                self._errors.pop('%s_date' % direction, None)
                self.cleaned_data['%s_date' % direction]=None
                self._errors.pop('%s_transport_type' % direction, None)
                self.cleaned_data['%s_transport_type' % direction]=None
        return self.cleaned_data

    class Meta:
        exclude = ['delegation_manager', 'user', 'claim_state', 'is_deleted',
                   'creation_date', 'is_synchronized', 'bill',
                   'additional_info', 'departure_charter_date']
        model = Claim


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel


class HotelRoomForm(forms.ModelForm):
    class Meta:
        model = HotelRoomCategory
        exclude = ('hotel', )


class StateForm(forms.Form):
    new_state = forms.IntegerField(widget=forms.HiddenInput)


class EmailMessageForm(forms.Form):
    subject = forms.CharField(label=_('subject'), max_length=255)
    body    = forms.CharField(label=_('body'), min_length=10,
            widget=forms.Textarea)


class ClaimsFilterForm(forms.Form):
    country = forms.ChoiceField(required=False, choices=get_countries(),
            label='Страна')
    region  = forms.ChoiceField(required=False, choices=get_regions(),
            label='Регион')
    need_hotel  = forms.BooleanField(required=False,
            label='Требуется гостиница')
    state  = forms.ChoiceField(required=False, choices=filters.FILTER_STATES,
            label='Статус заявки')
    is_sync = forms.ChoiceField(required=False, choices=filters.SYNC_STATES,
            label='Изменения')
    q = forms.CharField(required=False, label='Поиск')
    q2 = forms.CharField(required=False, label='Поиск по организации')
    charter_arrival   = forms.ChoiceField(required=False,
            choices=filters.CHARTER_CHOICES, label='Прибытие чартером')
    charter_arrival_date = forms.ChoiceField(required=False,
            choices=filters.CHARTER_ARRIVAL_DATE_CHOICES,
            label='Время прибытия чартером')
    charter_departure = forms.ChoiceField(required=False,
            choices=filters.CHARTER_CHOICES, label='Убытие чартером')
    # departure_charter_date = forms.ChoiceField(required=False,
    #        choices=filters.CHARTER_DATE_CHOICES, label='Дата чартера убытия')
    industry = forms.ChoiceField(label='Отрасль', required=False,
            choices=get_industries())
    claim_type = forms.ChoiceField(required=False,
            choices=filters.CLAIM_TYPE_CHOICES, label='Тип участника')
    is_registered = forms.ChoiceField(choices=(('', u'Все'), (1, u'Да'),
            (0, u'Нет')), label=u'Зарегистрирован', required=False)
    is_invited = forms.ChoiceField(choices=(('', u'Все'), (1, u'Да'),
            (0, u'Нет')), label=u'Приглашен', required=False)
    programm_type = forms.ChoiceField(required=False, label=u'Тип программы',
            choices=filters.PROGRAMM_CHOICES)




class ReserveForm(forms.Form):
    hotel           = forms.ChoiceField(choices=get_hotel_choices())
    room_class      = forms.ChoiceField(required=False)
    room_number     = forms.ChoiceField(required=False)
    arrival_date    = forms.DateTimeField(widget=forms.DateTimeInput, localize=True)
    departure_date  = forms.DateTimeField(widget=forms.DateTimeInput, localize=True)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)

        super(ReserveForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.fields['hotel'].initial = self.instance.room.hotel.id
            # Get all rooms for this hotel
            rooms = HotelRoomCategory.objects.filter(hotel=self.instance.room.hotel)
            # Populate room category
            class_choices, room_choices = {'':''}, {'':''}
            for c in rooms:
                if c.room_category not in class_choices:
                    class_choices[c.room_category] = c.get_room_category_display()
                if c.room_category == self.instance.room.room_category:
                    room_choices[c.id] = u"%s (%d чел.)" % (c.room_number, c.hotel_reserves.count())

            # Room category
            self.fields['room_class'].choices = class_choices.items()
            self.fields['room_class'].initial = self.instance.room.room_category
            # Room number
            self.fields['room_number'].choices = room_choices.items()
            self.fields['room_number'].initial = self.instance.room.id
            # Arrival/departure date and time
            self.fields['arrival_date'].initial   = self.instance.arrival_date
            self.fields['departure_date'].initial = self.instance.departure_date


class PaymentForm(forms.Form):
    sum  = forms.DecimalField(max_value=99999, max_digits=7, decimal_places=2)
    date = forms.DateField(widget=forms.DateInput)


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_("Username"), max_length=255)
