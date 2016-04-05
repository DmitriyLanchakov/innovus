# -*- coding: utf-8 -*-
from django.conf import settings
from profile.models import Country, Region, City, Claim

def countries(request):
    get = request.GET.get

    country = get('country__exact')
    available_countries = [
        i['country'] for i in Claim.objects.values('country').distinct()
    ]
    available_regions = [
        i['region'] for i in Claim.objects.values('region').exclude(region=None).distinct()
    ]


    return dict(
        countries = Country.objects.filter(pk__in=available_countries),
        regions = Region.objects.filter(country__exact=country,pk__in=available_regions),
#        cities = City.objects.filter(
#            country__exact = country,
#            region__exact  = region,
#        ),
    )


def registration_period(request):
    return {'REG_START': settings.REG_START, 'REG_END': settings.REG_END }

