# -*- coding: utf-8 -*-
from profile import settings as profile_settings


NEED_HOTEL = (
 ('', 'Все'),
 (-1, 'Не нужно'),
 (0,  'Нужно'),
 (-2, 'Не размещены'),
 (-3, 'Размещены'),
)

PROGRAMM_CHOICES = (
    ('', 'Все'),
) + profile_settings.PROGRAMM_TYPE_CHOICES

FILTER_STATES = (
    ('', 'Все'),
) + profile_settings.CLAIM_STATES + (
    ('-1', 'Оплаченные'),
    ('-2', 'Не отклонены')
)

CLAIM_STATES_ACTIONS = {
    profile_settings.CLAIM_WAITING_APPROVEMENT : 'Активировать заявку',
    profile_settings.CLAIM_WAITING_PAYMENT     : 'Платное участие',
    profile_settings.CLAIM_ACCEPTED            : 'Бесплатное участие',
    profile_settings.CLAIM_CANCELLED           : 'Отмена участия',
    profile_settings.CLAIM_REJECTED            : 'Отклонить заявку',
}
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
SYNC_STATES = (
    ('', 'Все'),
    ('1', 'Нет'),
    ('0', 'Есть'),
)


CHARTER_CHOICES = (
    ('', 'Все'),
    ('1', 'Требуется'),
    ('0', 'Не требуется'),
)

CHARTER_DEPARTURE_DATE_CHOICES = (
    ('', 'Все'),
) + profile_settings.DEPARTURE_CHARTER_CHOICES

CHARTER_ARRIVAL_DATE_CHOICES = (
    ('', 'Все'),
) + profile_settings.ARRIVAL_CHARTER_CHOICES

CLAIM_TYPE_CHOICES = (
    ('', 'Все'),
    (-1, '(не указано)'),
) + profile_settings.CLAIM_TYPE_CHOICES


CLAIM_TYPE_PART      = 1
CLAIM_TYPE_ORG       = 2
CLAIM_TYPE_VIP       = 3
CLAIM_TYPE_MASSMEDIA = 4
CLAIM_TYPE_SPEAKER = 5
CLAIM_TYPE_VIPSPEAKER = 6
CLAIM_TYPE_ATTENDANT = 7

CLAIM_TYPE_CHOICES = (
    ('', 'Все'),
    (CLAIM_TYPE_PART, 'Участник'),
    (CLAIM_TYPE_ORG,  'Организатор'),
    (CLAIM_TYPE_VIP,  'VIP'),
    (CLAIM_TYPE_MASSMEDIA, 'CМИ'),
    (CLAIM_TYPE_SPEAKER, 'Спикер'),
    (CLAIM_TYPE_VIPSPEAKER, 'VIP-спикер'),
    (CLAIM_TYPE_ATTENDANT, 'Сопровождающий'),
)

