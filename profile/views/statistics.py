# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from annoying.decorators import render_to

from profile.models import Claim, Country, Region


@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/by_registration.html')
def registration(request):
    countries =  Country.objects.filter(claims__in=Claim.objects.active()).order_by('title').distinct()
    regions = Region.objects.filter(claims__in=Claim.objects.active()).order_by('title').distinct()

    return {
        'total': Claim.objects.active(),
        'countries': countries,
        'regions': regions,
    }

