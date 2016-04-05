# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse

from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from openteam.utils import send_email

from profile.settings import *
from profile.forms import StateForm, HotelRoomForm, HotelForm, ActionForm, \
    ReserveForm
from profile.utils import ACTION_BINDING

from profile.models import Claim, Country, Hotel, HotelRoomCategory,\
    HotelRoomReserve, Industry, Region




# --------------------------------------------------------------------------- #

@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/settlers_list.html')
def settlers_list(request):
    hotels = []

    for hotel in Hotel.objects.all():
        hotel.total_populated = 0
        hotel.total = HotelRoomCategory.objects.filter(hotel=hotel).count()

        for cat_id, cat_title in HOTEL_CATEGORY_CHOICES:
            persons = HotelRoomReserve.objects.filter(
                room__in = HotelRoomCategory.objects.filter(hotel=hotel, room_category=cat_id)
            )

            setattr(hotel, 'column_%s' % cat_id, list(persons))

            hotel.total_populated += persons.count()

        hotels.append(hotel)

    return dict(
        hotels = hotels,
        manage_claim = True,
    )


# --------------------------------------------------------------------------- #

@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/by_countries.html')
def by_countries(request):
    countries = []

    for country in Country.objects.all():
        country.approved = Claim.objects.filter(country=country, claim_state=CLAIM_ACCEPTED).count()
        country.waiting_paiment = Claim.objects.filter(country=country, claim_state=CLAIM_WAITING_PAYMENT).count()

        if country.approved or country.waiting_paiment:
            countries.append(country)

            industries = []

            for industry in Industry.objects.all():
                industry.approved = Claim.objects.filter(country=country, industry=industry, claim_state=CLAIM_ACCEPTED).count()
                industry.waiting_paiment = Claim.objects.filter(country=country, industry=industry, claim_state=CLAIM_WAITING_PAYMENT).count()

                if industry.approved or industry.waiting_paiment:
                    industries.append(industry)

            if Claim.objects.filter(country=country, industry__isnull=True).count():
                industries.append (dict(
                    title = "Не указана",
                    approved = Claim.objects.filter(country=country, industry__isnull=True, claim_state=CLAIM_ACCEPTED).count(),
                    waiting_paiment = Claim.objects.filter(country=country, industry__isnull=True, claim_state=CLAIM_WAITING_PAYMENT).count(),
                ))

            country.industries = industries

    return dict(
        countries = countries,
        manage_claim = True,
    )

# --------------------------------------------------------------------------- #

@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/by_regions.html')
def by_regions(request):
    regions = []

    for region in Region.objects.all():
        region.approved = Claim.objects.filter(region=region, claim_state=CLAIM_ACCEPTED).count()
        region.waiting_paiment = Claim.objects.filter(region=region, claim_state=CLAIM_WAITING_PAYMENT).count()

        if region.approved or region.waiting_paiment:
            regions.append(region)

            industries = []

            for industry in Industry.objects.all():
                industry.approved = Claim.objects.filter(region=region, industry=industry, claim_state=CLAIM_ACCEPTED).count()
                industry.waiting_paiment = Claim.objects.filter(region=region, industry=industry, claim_state=CLAIM_WAITING_PAYMENT).count()

                if industry.approved or industry.waiting_paiment:
                    industries.append(industry)

            if Claim.objects.filter(region=region, industry__isnull=True).count():
                industries.append (dict(
                    title = "Не указана",
                    approved = Claim.objects.filter(region=region, industry__isnull=True, claim_state=CLAIM_ACCEPTED).count(),
                    waiting_paiment = Claim.objects.filter(region=region, industry__isnull=True, claim_state=CLAIM_WAITING_PAYMENT).count(),
                ))

            region.industries = industries

    return dict(
        regions = regions,
        manage_claim = True,
    )



# --------------------------------------------------------------------------- #
@login_required
@user_passes_test(lambda u: u.is_staff)
def action_process(request):
    form = ActionForm(request.POST or None)
    if form.is_valid():
        action_code = form.cleaned_data['action_code']
        ACTION_BINDING[action_code](request)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/state_change_fail.html')
def state_change(request, id):
    claim = get_object_or_404(Claim, pk=id)
    form = StateForm(request.POST or None)
    if form.is_valid():
        new_state = form.cleaned_data['new_state']
        if claim.change_state(new_state):
            send_email(claim.get_email,
                'state_changed',
                {'claim': claim},
            )
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return {'message': "невозможно изменить текущее состояние заявки"}
    else:
        return {'message': "недостаточно данных для изменения состояния"}


@login_required
@user_passes_test(lambda u: u.is_staff)
def synchronize(request, id):
    claim = get_object_or_404(Claim, pk=id, is_synchronized=False)
    if request.method == 'POST':
        claim.synchronize()
    return redirect('manage_claim_show',id=claim.id)


# --------------------------------------------------------------------------- #


@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/reserve.html')
def reserv_add(request, id):
    claim = get_object_or_404(Claim, pk=id)
    reserve = get_object_or_None(HotelRoomReserve, claim=claim)

    reserve_form = ReserveForm(request.POST or None, instance=reserve)
    if not reserve:
         reserve = HotelRoomReserve(claim=claim)

    if request.POST.get('room_number', None) and request.POST.get('arrival_date', None)  and request.POST.get('departure_date', None):
        reserve.room = HotelRoomCategory.objects.get(id = int(request.POST.get('room_number')))
        reserve.arrival_date = datetime.strptime(request.POST.get('arrival_date'), '%d.%m.%Y %H:%M')
        reserve.departure_date = datetime.strptime(request.POST.get('departure_date'), '%d.%m.%Y %H:%M')
        reserve.save()
        return redirect('manage_claim_show', id=claim.id)
    else:
        reserve_form.is_valid()

    return dict(
        claim = claim,
        reserve_form = reserve_form,
#        manage_claim = True,
    )

@login_required
@user_passes_test(lambda u: u.is_staff)
def reserve_remove(request, id):
    claim = get_object_or_404(Claim, pk=id)
    reserve = get_object_or_None(HotelRoomReserve, claim=claim)
    reserve.delete()
    return redirect(request.META.get('HTTP_REFERER', reverse('manage_claim_show', kwargs={'id': claim.id})))


# --------------------------------------------------------------------------- #
# hotels

@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/hotels/list.html')
def hotel_list(request):
    hotels = []

    for hotel in Hotel.objects.all():
        for cat_id, cat_title in HOTEL_CATEGORY_CHOICES:
            table = HotelRoomCategory.objects.filter(
                hotel         = hotel,
                room_category = cat_id,
            ).order_by('-price').values('price').annotate(
                count = Count('price')
            )
            setattr(hotel, 'column_%s' % cat_id, list(table))

        hotel.total = HotelRoomCategory.objects.filter(hotel=hotel).count()
        hotels.append(hotel)

    return dict(
        hotels = hotels,
        manage_hotel = True,
    )

@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/hotels/add.html')
def hotel_add(request):
    form = HotelForm(request.POST or None)

    if form.is_valid():
        hotel = form.save()
        return redirect('manage_hotel_change', hotel_id=hotel.pk)

    return dict(
        form = form,
        hotel_create = True,
    )



@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/hotels/change.html')
def hotel_change(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)

    filter = request.GET.get('filter', '-price')
    filter = filter if filter in ['room_number','room_category', 'name'] else 'room_category'
    rooms = HotelRoomCategory.objects.filter(hotel=hotel).order_by(filter, 'room_number')
    hotel_form = HotelForm(request.POST or None, instance=hotel)

    if hotel_form.is_valid():
        hotel_form.save()
        return redirect(request.path)

    return dict(
        hotel_form = hotel_form,
        room_form = HotelRoomForm(),
        rooms = rooms,
        hotel = hotel,
    )


@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/hotels/delete.html')
def hotel_delete(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)

    if request.method == 'POST':
        hotel.delete()
        return redirect('manage_hotel_list')

    return dict(
        hotel = hotel,
    )


@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/hotels/delete.html')
def room_delete(request, room_id):
    room = get_object_or_404(HotelRoomCategory, pk=room_id)
    hotel = room.hotel

    if request.method == 'POST':
        room.delete()
        return redirect('manage_hotel_change', hotel_id=hotel.id)

    return dict(
        hotel = hotel,
        room  = room,
    )


@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/hotels/add.html')
def room_add(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    form = HotelRoomForm(request.POST or None)

    if form.is_valid():
        room = form.save(commit=False)
        room.hotel = hotel
        room.save()
        return redirect('manage_hotel_change', hotel_id=hotel.pk)

    return dict(
        form = form,
        manage_hotel = True,
    )


@login_required
@user_passes_test(lambda u: u.is_staff)
@render_to('admin/claims/hotels/room_change.html')
def room_change(request, room_id):
    room = get_object_or_404(HotelRoomCategory, pk=room_id)
    room_form = HotelRoomForm(request.POST or None, instance=room)

    if room_form.is_valid():
        room = room_form.save()
        return redirect('manage_hotel_change', hotel_id=room.hotel.pk)
    return {'room_form': room_form}

