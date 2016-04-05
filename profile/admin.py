# -*- coding: utf-8 -*-
from annoying.decorators import render_to

from django.db import models
from django.db.models import Count
from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _
from publisher_admin.admin import SortableAdmin
from tinymce.widgets import TinyMCE

from profile.forms import StateForm
from profile.models import Claim, Country, Region, City, Industry, History, \
Hotel, HotelRoomCategory, HotelRoomReserve
from profile.utils import activation_resend as resend_method
from profile import settings as profile_settings
# --------------------------------------------------------------------------- #

class CityAdmin(admin.ModelAdmin):
    raw_id_fields = ['country', 'region']
    list_filter = ['country', ]
    search_fields = ['title', 'country__title', 'region__title']

class RegionAdmin(admin.ModelAdmin):
    raw_id_fields = ['country']
    list_filter = ['country', ]
    search_fields = ['title', 'country__title']

class CountryAdmin(admin.ModelAdmin):
    list_display = ['title', 'alpha2', 'alpha3', 'iso',  ]

class IndustryAdmin(admin.ModelAdmin):
    list_display = ['title', 'title_en']

# --------------------------------------------------------------------------- #

class IsNeedHotelFilterSpec(admin.filterspecs.ChoicesFilterSpec):
    """
    Собственный фильтр "По бронированию"
    """

    def __init__(self, f, request, params, model, model_admin):
        super(IsNeedHotelFilterSpec, self).__init__(f, request, params, model, model_admin)
        self.field_generic = '%s__' % self.field.name

        self.params = dict([(k, v) for k, v in params.items() if k.startswith(self.field_generic)])
        self.links  = (
            (_('All'), {}),
            (_('Yes'), {'%s__gte'   % self.field.name: str(1),}),
            (_('No'),  {'%s__exact' % self.field.name: str(0),}),
        )

    def title(self):
        """
        Заголовок фильтра
        """
        return _("Need hotel")

    def choices(self, cl):
        """
        Формирует список элементов фильтра
        """
        for title, param_dict in self.links:
            yield dict(
                selected     = self.params == param_dict,
                query_string = cl.get_query_string(param_dict, [self.field_generic]),
                display      = title
            )

# --------------------------------------------------------------------------- #

class ClaimAdmin(admin.ModelAdmin):
    actions       = ['activation_resend',]
    list_display  = ['last_name','first_name','middle_name', 'email', 'display_arrival',
        'display_departure', 'activation_code',]
    search_fields = ['first_name', 'last_name', 'email',]
    list_filter   = ['claim_state', 'need_hotel',]
    ordering      = ['last_name', 'first_name', 'middle_name',]
    fieldsets = [
        (None,
            {'fields': ['last_name', 'first_name', 'middle_name','gender', 'citizenship',],},),
        (_('Contacts'),
            {'fields': ['phone', 'phone_extra', 'fax', 'address', 'skype', 'icq', 'twitter', 'site', 'blog',],},),
        (_('Geography'),
            {'fields': ['country', 'region', 'city',],},),
        (_('Organization'),
            {'fields': ['industry', 'organization', 'position',],},),
        (_('Arrival'),
            {'fields': ['arrival_want_charter', 'arrival_transport_type', 'arrival_date',],},),
        (_('Departure'),
            {'fields': ['departure_want_charter', 'departure_transport_type', 'departure_date',],},),
        (_('Hotel information'),
            {'fields': ['need_hotel',],},),
        (_('State'),
            {'fields': ['claim_state',],},),
        (_('Delegation settings'),
            {'fields': ['is_take_part'],},),
        (_('Relations'),
            {'fields': ['user', 'delegation_manager'],},),
    ]

    # ----------------------------------------------------------------------- #

#    def get_urls(self):
#        return patterns('',
#            url(
#                regex  = '^$',
#                view   = self.admin_site.admin_view(self.custom_changelist_view),
#                name   = 'profile_claim_custom_changelist',
#            ),
#            url(
#                regex = '^(?P<claim_id>\d+)/view/$',
#                view  = self.admin_site.admin_view(self.claim_view),
#                name  = 'view_claim'
#            ),
#        ) + super(ClaimAdmin, self).get_urls() + patterns('',
#            url(
#                regex  = '^changelist/$',
#                view   = self.admin_site.admin_view(self.changelist_view),
#                name   = 'profile_claim_changelist',
#            ),
#
#            url(
#                regex = '^(?P<claim_id>\d+)/history/$',
#                view  = self.admin_site.admin_view(self.claim_history),
#                name  = 'claim_history'
#            ),
#        )

    def activation_resend(self, request, queryset):
        qs = queryset.filter(claim_state=profile_settings.CLAIM_SENT).exclude(user=None)
        resend_method(request, qs)

    @render_to('admin/profile/claim/claim_history.html')
    def claim_history(self, request, claim_id):
        """
        Список всех изменений заявки
        """
        claim = get_object_or_404(Claim, pk=claim_id)
        return {'claim': claim, 'opts': claim._meta,
                'app_label': claim._meta.app_label, 'original': claim,
                'changes': History.objects.filter(
                    claim=claim).order_by('-timestamp'),}


    def claim_update_state(self, request, claim_id):
        claim = get_object_or_404(Claim, pk=claim_id)
        if request.method == 'POST':
            state_form = StateForm(request.POST)

            if state_form.is_valid():
                state_change_result = claim.change_state(new_state=state_form.cleaned_data['new_state'])

                if state_change_result:
                    messages.success(request,
                        _('Claim state was succesfully updated: %(state)s' % {
                              'state': claim.get_claim_state_display(),
                              }
                        )
                    )

                else:
                    messages.error(request,
                        _('Claim state failed to update'),
                    )

        return redirect(request.META['HTTP_REFERER'])


    def display_hotel(self, obj):
        return _('No need') if obj.room_category == 0 \
            else obj.get_room_category_display()
    display_hotel.short_description = _('Hotel')


    def display_arrival(self, obj):
        return self._arrival_departure_info(obj, 'arrival')
    display_arrival.short_description = _('Arrival')


    def display_departure(self, obj):
        return self._arrival_departure_info(obj, 'departure')
    display_departure.short_description = _('Departure')


    def _arrival_departure_info(self, obj, direction):
        if getattr(obj, '%s_want_charter' % direction):
            return _('Charter')

        return _('%(date)s %(transport_type)s' % {
            'date' : getattr(obj, '%s_date' % direction),
            'transport_type': getattr(obj, 'get_%s_transport_type_display' % direction)(),
            }
        )


class HotelAdmin(admin.ModelAdmin):
    class RoomCategoryInline(admin.TabularInline):
        model = HotelRoomCategory
        extra = 2

    inlines = [RoomCategoryInline]
    list_display = [
        'name', 'display_total_rooms',
        'display_lux', 'display_appartment', 'display_studio',
        'display_1room1cat', 'display_2room1cat',
        'display_1room2cat', 'display_2room2cat',
    ]


    def display_total_rooms(self, hotel):
        return HotelRoomCategory.objects.filter(hotel=hotel).count()


    def display_room_category_count(self, hotel, room_category):
        table = HotelRoomCategory.objects.filter(
            hotel=hotel,
            room_category=room_category
        ).order_by('-price').values('price').annotate(count=Count('price'))

        body = ''.join(['<li>%(price)s / %(count)s</li>' % i for i in table])

        if body:
            return '<ul>' + body  + '</ul>'
        return '-'


    def display_lux(self, obj):
        return self.display_room_category_count(obj, profile_settings.HOTEL_CATEGORY_LUX)
    display_lux.short_description = _('Luxes')
    display_lux.allow_tags = True


    def display_appartment(self, obj):
        return self.display_room_category_count(obj, profile_settings.HOTEL_CATEGORY_APPARTMENT)
    display_appartment.short_description = _('Appartments')
    display_appartment.allow_tags = True


    def display_studio(self, obj):
        return self.display_room_category_count(obj, profile_settings.HOTEL_CATEGORY_STUDIO)
    display_studio.short_description = _('Studios')
    display_studio.allow_tags = True


    def display_1room1cat(self, obj):
        return self.display_room_category_count(obj, profile_settings.HOTEL_CATEGORY_1MEST1CAT)
    display_1room1cat.short_description = _('1 mest 1 kat')
    display_1room1cat.allow_tags = True


    def display_2room1cat(self, obj):
        return self.display_room_category_count(obj, profile_settings.HOTEL_CATEGORY_2MEST1CAT)
    display_2room1cat.short_description = _('2 mest 1 kat')
    display_2room1cat.allow_tags=True


    def display_1room2cat(self, obj):
        return self.display_room_category_count(obj, profile_settings.HOTEL_CATEGORY_1MEST2CAT)
    display_1room2cat.short_description = _('1 mest 2 kat')
    display_1room2cat.allow_tags=True


    def display_2room2cat(self, obj):
        return self.display_room_category_count(obj, profile_settings.HOTEL_CATEGORY_2MEST2CAT)
    display_2room2cat.short_description = _('2 mest 2 kat')
    display_2room2cat.allow_tags=True


class HotelRoomCategoryAdmin(admin.ModelAdmin):
    list_display = ['room_category', 'price', 'hotel']


class HotelRoomReserveAdmin(admin.ModelAdmin):
    raw_id_fields = ['claim', 'room']


class HistoryAdmin(admin.ModelAdmin):
    list_filter = ['claim', ]
    ordering = ['timestamp', ]

#
#class ClaimEventAdmin(admin.ModelAdmin):
#    raw_id_fields = ['claim', 'event']
#    list_display = ['claim', 'event']
#    list_filter = ['event']
#
#class EventAdmin(SortableAdmin):
#    list_display = ['title', 'sort_order', 'display_count']
#    formfield_overrides = {models.TextField: { 'widget' : TinyMCE }, }
#    list_filter = ['event_type']
#    ordering = ['date_started', 'event_type', 'sort_order']
#
#
#    def display_count(self, obj):
#        return ClaimEvent.objects.filter(event=obj).count()


admin.site.register(City, CityAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(Claim, ClaimAdmin)
admin.site.register(History, HistoryAdmin)
#admin.site.register(ClaimEvent, ClaimEventAdmin)


admin.site.register(Hotel, HotelAdmin)
#admin.site.register(Event, EventAdmin)
admin.site.register(HotelRoomCategory, HotelRoomCategoryAdmin)
admin.site.register(HotelRoomReserve, HotelRoomReserveAdmin)


admin.filterspecs.FilterSpec.filter_specs.insert(0,
    (lambda f: f.name == 'room_category', IsNeedHotelFilterSpec)
)

