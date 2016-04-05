# encoding: utf-8
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from ho import pisa
import cStringIO
from openteam.utils import send_email
from profile import models
from profile import settings as profile_settings


def activation_resend(request, qs=None):
    if not qs:
        qs = models.Claim.objects.filter(claim_state=profile_settings.CLAIM_SENT).exclude(user=None)
    for claim in qs:
        if claim.activation_code == u'активирован':
            claim.generate_code()

        send_email(claim.user.username, 'registration', {
            'code': claim.activation_code})



def reservation_resend(request):
    claim_id = request.POST.get('claim_id', None)
    claim = get_object_or_404(models.Claim, id=int(claim_id))
    reserve = models.HotelRoomReserve.objects.get(claim=claim)
    send_email(claim.get_email, 'reserve_added', {
        'claim': claim,
        'reserve': reserve,
        'changed': True,
    })



ACTION_BINDING = {
    profile_settings.ACTION_RESEND_ACTIVATION: activation_resend,
    profile_settings.ACTION_RESEND_RESERVATION: reservation_resend,
}



def get_hotel_choices():
    from profile.models import Hotel
    response = [('', '')]
    for hotel in Hotel.objects.all().order_by('name'):
        response.append((hotel.id, hotel.name))
    return response


def get_hotel_rooms():
    from profile.models import HotelRoomCategory
    rooms = HotelRoomCategory.objects.all()
    return [ [room.pk, room.get_room_category_display()] for room in rooms ]


def generate_bill(request, claim):
    template = render_to_string('profile/payment.html',{
        'media_root': settings.MEDIA_ROOT,
        'claim': claim,
        'cost_numeric': settings.COST1_NUMERIC if claim.creation_date < settings.DATE_X else settings.COST2_NUMERIC,
        'cost_verbose': settings.COST1_VERBOSE if claim.creation_date < settings.DATE_X else settings.COST2_VERBOSE,},
        RequestContext(request))
    result = cStringIO.StringIO()
    pdf = pisa.pisaDocument(template.encode("utf-8"), result, show_error_as_pdf = True, encoding='utf-8')
    if not pdf.err:
        return result.getvalue()
    else:
        return None


def get_filtered_claims(data):
    claims = models.Claim.objects.all()
    filter_set = dict()

    if data.get('q', None):
        q = data['q']
        claims = claims.filter(last_name__istartswith=q)
        filter_set[u'поиск по запросу'] = q

    if data.get('q2', None):
        q2 = data['q2']
        claims = claims.filter(organization__istartswith=q2)
        filter_set[u'поиск по организации'] = q2


    if data.get('country', None):
        if data['country'] == '-1':
            claims = claims.exclude(country__pk=profile_settings.RUSSIA_COUNTRY_ID)
            filter_set[u'страна'] = u'не Россия'

        else:
            claims = claims.filter(country__pk=data['country'])
            filter_set[u'страна'] = models.Country.objects.get(pk = data['country'])

    if data.get('region', None):
        claims = claims.filter(region__pk=data['region'])
        filter_set[u'регион'] = models.Region.objects.get(pk = data['region'])

    if data.get('state', None):
        state = data['state']
        if state == '-1':

            claims = claims.filter(
                claim_state = profile_settings.CLAIM_ACCEPTED,
                payment_date__isnull = False,
                payment_sum__isnull  = False,
            )
            filter_set[u'состояние заявки'] = u'Оплачена'
        elif state == '-2':
            claims = claims.exclude(
                claim_state__in = [ profile_settings.CLAIM_CANCELLED, profile_settings.CLAIM_REJECTED ]
            )
            filter_set[u'состояние заявки'] = u'Не отклонена и не отменена'
        else:
            claims = claims.filter(claim_state = state)
            filter_set[u'состояние заявки'] = unicode(profile_settings.CLAIM_STATES[int(data['state'])][1])


    if data.get('is_registered', None):
        if data['is_registered'] == '0':
            claims = claims.unregistered()
            filter_set[u'зарегистрирован'] = u'Нет'
        elif data['is_registered'] == '1':
            claims = claims.registered()
            filter_set[u'зарегистрирован'] = u'Да'


    if data.get('is_invited', None):
        if data['is_invited'] == '0':
            claims = claims.filter(is_invited=False)
            filter_set[u'приглашен'] = u'Нет'
        elif data['is_invited'] == '1':
            claims = claims.filter(is_invited=True)
            filter_set[u'приглашен'] = u'Да'

    if data.get('need_hotel', None):
        claims = claims.filter(need_hotel=data['need_hotel'])

    if data.get('programm_type', None):
        claims = claims.filter(programm_type=data['programm_type'])

#    if data.get('hotel', None):
#
#        if data['hotel'] == '-1':
#            claims = claims.filter(Q(room_category__isnull = True) | Q(room_category = 0))
#            filter_set[u'бронирование гостиницы'] = u'не требуется'
#
#        elif data['hotel'] == '0':
#            claims = claims.filter(Q(room_category__isnull = False) & Q(room_category__gt =  0))
#            filter_set[u'бронирование гостиницы'] = u'требуется'
#
#        # Не размещены
#        elif data['hotel'] == '-2':
#            hosted = [i['claim'] for i in HotelRoomReserve.objects.values('claim')]
#
#            claims = claims.filter(
#                Q(room_category__isnull = False) & \
#                Q(room_category__gt     = 0)
#            ).exclude(pk__in=hosted)
#            filter_set[u'бронирование гостиницы'] = u'Не размещены'
#
#        # Размещены
#        elif data['hotel'] == '-3':
#
#            hosted = [i['claim'] for i in HotelRoomReserve.objects.values('claim')]
#            claims = claims.filter(
#                Q(room_category__isnull = False) & \
#                Q(room_category__gt     = 0)
#            ).filter(pk__in=hosted)
#
#            filter_set[u'бронирование гостиницы'] = u'Размещены'
#
#
#        #
#        else:
#            claims = claims.filter(room_category = int(data['hotel']))
#            n_type = ''
#            for num, title in HOTEL_CATEGORY_CHOICES:
#                if num == int(data['hotel']):
#                    n_type = title
#                    break
#
#            filter_set[u'бронирование гостиницы'] = u'требуется и тип номера '+ unicode(n_type)

    if data.get('is_sync', None):
        flag = data['is_sync']
        if flag.isdigit():
            claims = claims.filter(is_synchronized= bool(int(flag)))
        if '1' == data['is_sync']:
            filter_set[u'изменений'] = u'нет'
        elif '0' == data['is_sync']:
            filter_set[u'изменения'] = u'есть'

    if data.get('charter_arrival'):
        charter = data['charter_arrival']
        claims = claims.filter(arrival_want_charter = bool(int(charter)))
        filter_set[u'Прибытие чартером'] = 'требуется' if bool(int(charter)) else 'не требуется'

    if data.get('charter_departure'):
        charter = data['charter_departure']
        claims = claims.filter(departure_want_charter = bool(int(charter)))
        filter_set[u'Убытие чартером'] = 'требуется' if bool(int(charter)) else 'не требуется'

    if data.get('departure_charter_date'):
        charter_date = data['departure_charter_date']
        claims = claims.filter(departure_charter_date=int(charter_date))

    if data.get('charter_arrival_date'):
        date = data['charter_arrival_date']
        claims = claims.filter(arrival_charter_date=int(date))

    if data.get('industry'):
        industry = data['industry']
        claims = claims.filter(industry=industry)
        filter_set[u'Отрасль'] = unicode(industry)

    if data.get('claim_type'):
        claim_type = data['claim_type']
        label = '(не указано)'
        if claim_type.isdigit() or claim_type == '-1':
            claim_type = int(claim_type)
        for v,l in profile_settings.CLAIM_TYPE_CHOICES:
            if v == claim_type:
                label = l
                break

        if claim_type >= 0:
            claims = claims.filter(claim_type=claim_type)
        elif claim_type == -1:
            claims = claims.filter(claim_type__isnull=True)
        filter_set[u'Тип участника'] = label



    return claims.order_by('last_name', 'first_name', 'middle_name', 'email'), filter_set





def get_countries():
    choice_list = [('', 'Все'), ('-1', 'Не Россия')]
    countries =  models.Country.objects.filter(claims__in=models.Claim.objects.all()).distinct()
    for country in countries:
        choice_list.append((country.id, country.title))

    return choice_list

def get_regions():
    choice_list = [('', 'Все'), ]
    regions = models.Region.objects.filter(claims__in=models.Claim.objects.all()).distinct()
    for r in regions:
        choice_list.append((r.id, r.title))
    return choice_list


def get_industries():
    choice_list = [('', 'Все'), ]
    industries = models.Industry.objects.filter(claims__in=models.Claim.objects.all()).distinct()
    for i in industries:
        choice_list.append((i.id, i.title))
    return choice_list

