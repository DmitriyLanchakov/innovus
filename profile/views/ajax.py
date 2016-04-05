# -*- coding: utf-8 -*-
'''
Created on 29.04.2010

@author: nimnull
'''
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.translation import ugettext as _

from annoying.decorators import ajax_request, JsonResponse

from profile.models import Region, Claim, City, HotelRoomCategory
from profile import settings as profile_settings


@ajax_request
def check_email(request):
    email = request.GET.get('email', '')
    free  = User.objects.filter(is_active=True,email=email).count() == 0

    if free:
        message = _('E-mail %s is available' % email)

    else:
        message = _('E-mail %s already used' % email)

    return {'email': email, 'free': free, 'message': message}

# --------------------------------------------------------------------------- #

@ajax_request
def regions_filter(request):
    country  = request.GET.get('country') or request.GET.get('country__exact')
    region   = request.GET.get('region') or request.GET.get('region__exact')

    queryset = Region.objects.filter(country__pk=country).order_by('title')

    if request.GET.get('country__exact'):
        available_regions = [i['region'] for i in Claim.objects.values('region').exclude(region=None).distinct()]
        queryset = queryset.filter(pk__in=available_regions)


    if region:
        queryset = City.objects.filter(region__exact=region).order_by('title')

    result = ""
    for i in queryset:
        result += "<option value='%d'>%s</option>" % (i.id, i.title)

    return HttpResponse(result)


@ajax_request
def get_hotel_categories(request, id):
    categories = HotelRoomCategory.objects.filter(hotel__id = id).values('room_category').distinct()
    categories = [ i['room_category'] for i in categories ]
    response = []

    for item in profile_settings.HOTEL_CATEGORY_CHOICES:
        if item[0] in categories:
            response.append([ item[0], unicode(item[1]) ])

    return JsonResponse(response)


@ajax_request
def get_room_by_categy(request, hotel_id, cat_id):
     rooms = HotelRoomCategory.objects.filter(hotel__id = hotel_id).filter(room_category = cat_id)
     rooms = [ {'id': room.pk, 'value': u"%s (%d чел.)" % (room.room_number, room.hotel_reserves.count())  } for room in rooms ]
     return JsonResponse(rooms)

