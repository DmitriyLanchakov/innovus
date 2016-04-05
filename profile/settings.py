# -*- coding: utf-8 -*-
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
# ------------------------------------------------------------------------------
CLAIM_SENT                  = 0
CLAIM_WAITING_APPROVEMENT   = 1
CLAIM_WAITING_PAYMENT       = 2
CLAIM_ACCEPTED              = 3
CLAIM_CANCELLED             = 4
CLAIM_REJECTED              = 5

CLAIM_STATES = (
    (CLAIM_SENT, _('Claim sent')),
    (CLAIM_WAITING_APPROVEMENT, _('Waiting for approvement')),
    (CLAIM_WAITING_PAYMENT, _('Waiting for payment')),
    (CLAIM_ACCEPTED, _('Accepted')),
    (CLAIM_CANCELLED, _('Cancelled')),
    (CLAIM_REJECTED, _('Rejected')),
)
# ------------------------------------------------------------------------------

TOMSK_REGION_ID   = 70

TRANSPORT_CHARTER  = 1
TRANSPORT_BUS      = 2
TRANSPORT_RAILROAD = 3
TRANSPORT_AVIA     = 4
TRANSPORT_ANOTHER  = 5

EVENT_TYPE_CHOICES = (
    (1, _('Panel discussions')),
    (2, _('Debating club')),
    (3, _('Round table')),
    (4, _('Plenary')),
)

TRANSPORT_CHOICES = (
    (TRANSPORT_BUS,      _('Bus')),
    (TRANSPORT_RAILROAD, _('Train')),
    (TRANSPORT_AVIA,     _('Aircraft')),
    (TRANSPORT_ANOTHER,  _('Another transport')),
)

WANT_YES=1
WANT_NO=0

WANT_CHOICES = (
    (WANT_NO, _('No')),
    (WANT_YES, _('Yes')),
)

# ------------------------------------------------------------------------------

RUSSIA_COUNTRY_ID = 170
TOMSK_CITY_ID     = 853

# ------------------------------------------------------------------------------

REQUESTED_ABSENT = 0
REQUEST_SENT = 1
REQUEST_PROCESSED = 2

PERSONAL_INFO_REQUEST = (
    (REQUESTED_ABSENT, u'не выполнялся'),
    (REQUEST_SENT, u'отправлен'),
    (REQUEST_PROCESSED, u'информация получена'),
)

HOTEL_CATEGORY_APPARTMENT = 1
HOTEL_CATEGORY_LUX        = 2
HOTEL_CATEGORY_STUDIO     = 3
HOTEL_CATEGORY_1MEST1CAT  = 4
HOTEL_CATEGORY_2MEST1CAT  = 5
HOTEL_CATEGORY_1MEST2CAT  = 6
HOTEL_CATEGORY_2MEST2CAT  = 7

HOTEL_CATEGORY_CHOICES = (
    (HOTEL_CATEGORY_APPARTMENT, _('Appartment')),
    (HOTEL_CATEGORY_LUX,        _('Lux')),
    (HOTEL_CATEGORY_STUDIO,     _('Studio')),
    (HOTEL_CATEGORY_1MEST1CAT,  _('1 mest 1 kat')),
    (HOTEL_CATEGORY_2MEST1CAT,  _('2 mest 1 kat')),
    (HOTEL_CATEGORY_1MEST2CAT,  _('1 mest 2 kat')),
    (HOTEL_CATEGORY_2MEST2CAT,  _('2 mest 2 kat')),
)
# ------------------------------------------------------------------------------


GENDER_CHOICES = (
    (1, _('Male')),
    (2, _('Female')),
)

TAKE_PART_P = 1
TAKE_PART_CONTACT_WO_P = 2
TAKE_PART_CONTACT_W_P = 3
TAKE_PART_DELEGATE = 4

TAKE_PART_CHOICES = (
    (TAKE_PART_P, _('Participant')),
    (TAKE_PART_CONTACT_WO_P, _('Contact without participation')),
    (TAKE_PART_CONTACT_W_P, _('Contact with participation')),
    (TAKE_PART_DELEGATE, _('Delegate')),
)


CLAIM_TYPE_PART      = 1
CLAIM_TYPE_ORG       = 2
CLAIM_TYPE_VIP       = 3
CLAIM_TYPE_MASSMEDIA = 4
CLAIM_TYPE_SPEAKER = 5
CLAIM_TYPE_VIPSPEAKER = 6
CLAIM_TYPE_ATTENDANT = 7

CLAIM_TYPE_CHOICES = (
    (CLAIM_TYPE_PART, 'Участник'),
    (CLAIM_TYPE_ORG,  'Организатор'),
    (CLAIM_TYPE_VIP,  'VIP'),
    (CLAIM_TYPE_MASSMEDIA, 'CМИ'),
    (CLAIM_TYPE_SPEAKER, 'Спикер'),
    (CLAIM_TYPE_VIPSPEAKER, 'VIP-спикер'),
    (CLAIM_TYPE_ATTENDANT, 'Сопровождающий'),
)

CHARTER_DATE1 = 1
CHARTER_DATE2 = 2

DEPARTURE_CHARTER_CHOICES = (
    (CHARTER_DATE1, _('May 27, 2011 on 10pm')),
    (CHARTER_DATE2, _('May 27, 2011 on 11pm')),
)

ARRIVAL_CHARTER_CHOICES = (
    (CHARTER_DATE1, _('May 25, 2011 on 6pm')),
    (CHARTER_DATE2, _('May 25, 2011 on 9pm')),
)

TRANSPORT_NONE     = 1
TRANSPORT_BUS      = 2
TRANSPORT_RAILROAD = 3
TRANSPORT_AVIA     = 4
TRANSPORT_ANOTHER  = 5

ACTION_RESEND_ACTIVATION = 1
ACTION_RESEND_RESERVATION = 2

ACTIONS = (
    (ACTION_RESEND_ACTIVATION, u'реактивация'),
    (ACTION_RESEND_RESERVATION, u'уведомить о заселении'),
)

PROGRAMM_TYPE_YOUTH = 'youth'
PROGRAMM_TYPE_GENERAL = 'general'
PROGRAMM_TYPE_CHOICES = (
    (PROGRAMM_TYPE_YOUTH, _('programm youth')),
    (PROGRAMM_TYPE_GENERAL, _('programm general')),
)

