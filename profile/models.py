# -*- coding: utf-8 -*-

from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from hashlib import md5

from time import time
from annoying.functions import get_object_or_None
from cms.models import CMSPlugin
from openteam.utils import send_email

from profile import settings as profile_settings
from profile.managers import ClaimManager

from events.models import ForumEvent


class Country(models.Model):
    title = models.CharField(_('Country'), max_length=255,)
    title_en = models.CharField(_('Country'), max_length=255, default='')
    alpha2  = models.CharField(max_length=255, default='') # max=2, but...
    alpha3  = models.CharField(max_length=255, default='') # max=3, but...
    iso     = models.CharField(max_length=255, default='') # max=3, but...

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'profile'
        ordering = ('title', )
        verbose_name = _('country')
        verbose_name_plural = _('countries')


class Region(models.Model):
    title   = models.CharField(max_length=255, verbose_name=_('Region'))
    country = models.ForeignKey(Country, related_name='regions')


    def __unicode__(self):
        return self.title


    class Meta:
        app_label = 'profile'
        ordering = ('title', )
        verbose_name = _('region')
        verbose_name_plural = _('regions')


class City(models.Model):
    title   = models.CharField(max_length=255, verbose_name=_('City'))
    country = models.ForeignKey(Country, related_name='cities')
    region  = models.ForeignKey(Region, related_name='cities')


    def __unicode__(self):
        return self.title


    class Meta:
        app_label = 'profile'
        ordering = ('title', )
        verbose_name = _('city')
        verbose_name_plural = _('cities')


class Industry(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('title ru'))
    title_en = models.CharField(max_length=255, default='', verbose_name=_('title en'))
    sort_order = models.IntegerField(_('sort order'), default=100)

    def __unicode__(self):
        return self.title


    class Meta:
        ordering = ['sort_order', 'title', 'title_en']
        verbose_name_plural = _('Industries')


class Claim(models.Model):
    country = models.ForeignKey(Country, related_name='claims',
        blank=True, null=True, verbose_name=_('country'))
    region = models.ForeignKey(Region, related_name='claims',
        blank=True, null=True, verbose_name=_('region'))
    city = models.ForeignKey(City, related_name = 'claims',
        blank=True, null=True, verbose_name=_('city'))
    delegation_manager  = models.ForeignKey('self',
        null=True, blank=True, related_name='delegates')
    user = models.ForeignKey(User, null=True, blank=True, related_name='claims')
    activation_code = models.CharField(null=True, blank=True, editable=False,
        max_length=255)
    bill = models.FileField(_('bill'), upload_to='bills', null=True)
    bill_date = models.DateTimeField(blank=True,null=True)
    citizenship = models.CharField(_('citizenship'), max_length=255, default='')
    claim_state = models.IntegerField(_('request state'), choices=profile_settings.CLAIM_STATES,
        default=profile_settings.CLAIM_SENT, db_index=True)
    creation_date = models.DateTimeField(default=datetime.now, null=True, blank=True)
    first_name = models.CharField(max_length=255, verbose_name=_('first name'))
    gender = models.IntegerField(_('gender'), 
        choices=profile_settings.GENDER_CHOICES)
    is_take_part = models.IntegerField(_('taking part?'), 
        choices=profile_settings.TAKE_PART_CHOICES, blank=True)
    last_name  = models.CharField(_('last name'), max_length=255)
    middle_name = models.CharField(_('middle name'), max_length=255,
        blank=True, default='')
    phone = models.CharField(_('mobile phone'), max_length=255,
        blank=True, null=True)
    phone_extra = models.CharField(_('work phone'), max_length=255, blank=True, default='')
    email = models.EmailField(_('Your email'), max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, default='',
        verbose_name=_('address'))
    fax   = models.CharField(max_length=255,   blank=True, default='',
        verbose_name=_('fax'))
    skype = models.CharField(max_length=255,   blank=True, default='')
    icq   = models.CharField(max_length=9,     blank=True, default='')
    site  = models.URLField(max_length=255,    blank=True, default='',
        verbose_name=_('site'))
    blog  = models.URLField(max_length=255,    blank=True, default='',
        verbose_name=_('blog'), verify_exists=False)
    twitter = models.CharField(max_length=255, blank=True, default='')
    programm_type = models.CharField(_('programm type'), max_length=256,
        choices=profile_settings.PROGRAMM_TYPE_CHOICES,
        default=profile_settings.PROGRAMM_TYPE_GENERAL)
    # room_category   = models.IntegerField(choices=HOTEL_CATEGORY_CHOICES,blank=True, null=True, verbose_name=_('room class'))
    need_hotel = models.BooleanField(_('need reservation'), default=False)
    # Personal
    claim_type = models.IntegerField(choices=profile_settings.CLAIM_TYPE_CHOICES,
        blank=True, default=profile_settings.CLAIM_TYPE_PART, null=True)
    # Company
    industry     = models.ForeignKey(Industry, related_name='claims', 
        blank=True, null=True, verbose_name=_('industry'))
    organization = models.CharField(_('organization'), max_length=255, null=True)
    position     = models.CharField(_('position'), max_length=255, null=True)

    # Arrival info
    arrival_want_charter   = models.IntegerField(
        choices=profile_settings.WANT_CHOICES,
        blank=True,
        verbose_name=_('charter for arrival')
    )
    arrival_charter_date = models.IntegerField(_('arrival charter date'),
        choices=profile_settings.ARRIVAL_CHARTER_CHOICES,
        null=True, blank=True)
    arrival_transport_type = models.IntegerField(
        choices=profile_settings.TRANSPORT_CHOICES,
        blank=True,
        null =True,
        verbose_name=_('arrival transport')
    )
    arrival_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('arrival date'),

    )
    # Departure info
    departure_want_charter = models.IntegerField(
        choices=profile_settings.WANT_CHOICES,
        blank=True,
        verbose_name=_('charter for departure')
    )
    departure_charter_date = models.IntegerField(_('departure charter date'),
        choices=profile_settings.DEPARTURE_CHARTER_CHOICES,
        null=True, blank=True)
    departure_transport_type = models.IntegerField(_('departure transport'),
        choices=profile_settings.TRANSPORT_CHOICES, blank=True, null=True)
    departure_date = models.DateTimeField(_('departure date'), blank=True,
        null=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    # State
    is_synchronized = models.BooleanField(_('Is syncronized?'), default=True)
    additional_info = models.IntegerField(_('request personal info'),
        default=profile_settings.REQUESTED_ABSENT,
        choices=profile_settings.PERSONAL_INFO_REQUEST)
    # Payment stuff
    payment_date = models.DateField(blank=True, null=True)
    payment_sum  = models.DecimalField(blank=True, null=True, decimal_places=2,
            max_digits=7)
    #
    is_registered = models.BooleanField(default=False)
    is_invited = models.BooleanField(default=False)
    events = models.ManyToManyField(ForumEvent, null=True, blank=True, related_name='registered')

    objects = ClaimManager()

    def is_waiting_payment(self):
        return self.claim_state == profile_settings.CLAIM_WAITING_PAYMENT

    def payment(self, money, date):
        #if not self.is_waiting_payment():
        if not (self.is_waiting_payment() or self.payment_date):
            from profile.exceptions import IncorrectClaimStateException
            raise IncorrectClaimStateException(
                "Can't make payment if state != %s" % profile_settings.CLAIM_WAITING_PAYMENT
            )

        self.payment_date = date
        self.payment_sum  = money
        self.claim_state = profile_settings.CLAIM_ACCEPTED
        self.save()

    def activate(self):
        if self.user and not self.user.is_active:
            self.user.is_active = True
#            self.activation_code = u'активирован'
            self.claim_state = profile_settings.CLAIM_WAITING_APPROVEMENT
            self.user.save()
            self.save()
            return True
        else:
            return False


    def change_state(self, new_state, commit=True):
        if new_state in self.next_states:
            self.claim_state = new_state
            if commit:
                self.save()
            return True
        else:
            return False

    @property
    def next_states(self):
        next_states = {
           profile_settings.CLAIM_SENT: [
                   profile_settings.CLAIM_WAITING_APPROVEMENT,
                   profile_settings.CLAIM_CANCELLED,
                   profile_settings.CLAIM_REJECTED ],
           profile_settings.CLAIM_WAITING_APPROVEMENT: [
                   profile_settings.CLAIM_WAITING_PAYMENT,
                   profile_settings.CLAIM_ACCEPTED,
                   profile_settings.CLAIM_REJECTED,
                   profile_settings.CLAIM_CANCELLED ],
           profile_settings.CLAIM_WAITING_PAYMENT: [
                   profile_settings.CLAIM_ACCEPTED,
                   profile_settings.CLAIM_REJECTED,
                   profile_settings.CLAIM_CANCELLED ],
           profile_settings.CLAIM_ACCEPTED: [
                   profile_settings.CLAIM_REJECTED,
                   profile_settings.CLAIM_CANCELLED ],
           profile_settings.CLAIM_CANCELLED: [],
           profile_settings.CLAIM_REJECTED: [],
        }

        return next_states[self.claim_state]


    def get_bill(self, request):
        from profile.utils import generate_bill
        return generate_bill(request, self)
        # return self.bill


    @property
    def get_email(self):
        return self.delegation_manager.email if self.delegation_manager else self.email


    def generate_code(self):
        self.activation_code = md5("%s-%s" % (time(), settings.SECRET_KEY)).hexdigest()
        self.save()

    @property
    def is_travel(self):
        return self.region_id != profile_settings.TOMSK_REGION_ID

    def synchronize(self):
        self.is_synchronized = True
        self.save()


    def save(self, *args, **kwargs):
        if self.user and not self.activation_code:
            self.activation_code = md5("%s-%s" % (time(), settings.SECRET_KEY)).hexdigest()

        super(Claim, self).save(*args, **kwargs)

#    @property
#    def want_reserve(self):
#        return self.room_category != 0


    def __unicode__(self):
        return unicode(' ').join([self.first_name, self.middle_name , self.last_name])

    class Meta:
        verbose_name = _('claim')
        verbose_name_plural = _('claims')

class History(models.Model):
    """
    History of claim changes
    """
    claim        = models.ForeignKey(Claim, related_name='histories', null=True)
    user         = models.ForeignKey(User, related_name='histories', blank=True, null=True)
    field_name   = models.CharField(max_length=255,)
    value_before = models.TextField(blank=True, null=True)
    value_after  = models.TextField(blank=True, null=True)
    timestamp    = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return unicode(_(u"""%(claim)s: %(field_name)s changed
        from %(before)s to %(after)s on %(timestamp)s""" % \
            dict(
                claim       = self.claim,
                field_name  = self.field_name,
                before      = self.value_before or _('(nothing)'),
                after       = self.value_after or _('(nothing)'),
                timestamp   = self.timestamp,
            )
        ))

    class Meta:
        verbose_name = _('claim change')
        verbose_name_plural = _('claims change')


def log_model_changes_pre_save(sender, **kwargs):
    new = kwargs['instance']
    old = get_object_or_None(sender, pk=new.pk)

    if old:
        changes = []
        important_fields = [
            'arrival_want_charter',
            'departure_want_charter',
            'arrival_transport_type',
            'departure_transport_type',
            'arrival_date',
            'departure_date',
            'room_category',
        ]

        for field in old._meta.fields:
            before = field.value_to_string(old)
            after  = field.value_to_string(new)

            if before != after:
                # choices fields
                if field.choices:
                    before = getattr(old, 'get_%s_display' % field.name)()
                    after  = getattr(new, 'get_%s_display' % field.name)()

                # related fields
                elif isinstance(field, models.ForeignKey) :
                    before = unicode(getattr(old, field.name))
                    after  = unicode(getattr(new, field.name))

                changes.append(
                    dict(
                        before = before,
                        after  = after,
                        field  = field.name,
                    )
                )

                # most important fields!
                if field.name in important_fields:
                    new.is_synchronized = False


                History.objects.create(
                    claim        = old,
                    field_name   = field.name,
                    value_before = before,
                    value_after  = after,
                )
        #
        if changes:
            send_email(settings.NOTIFY_EMAIL, 'change_claim',
                dict(
                    new = new,
                    old = old,
                    changes = changes,
                )
            )

def delete_hotel_reserve_when_claim_cancelled_or_rejected(sender, **kwargs):
    instance = kwargs['instance']

    if instance.claim_state in [profile_settings.CLAIM_CANCELLED, profile_settings.CLAIM_REJECTED]:
        to_delete = HotelRoomReserve.objects.filter(claim=instance)
        to_delete.delete()

models.signals.pre_save.connect(log_model_changes_pre_save, sender=Claim)
models.signals.post_save.connect(delete_hotel_reserve_when_claim_cancelled_or_rejected, sender=Claim)
setattr(settings, 'AUTH_PROFILE_MODULE', 'profile.Claim')


class Registration(CMSPlugin):
    template = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('template'))
    title    = models.CharField(max_length=255, blank=True, default='', verbose_name=_('title'))


class Participants(CMSPlugin):
    template = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('template'))
    title    = models.CharField(max_length=255, blank=True, default='', verbose_name=_('title'))
    per_page = models.IntegerField(default=10, blank=True)


class Hotel(models.Model):
    """
    Hotel room categories distribution
    """
    name = models.CharField(max_length=255, verbose_name=_('Hotel name'))

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'profile'
        ordering = ['name']
        verbose_name = _('hotel')
        verbose_name_plural = _('hotels')


class HotelRoomCategory(models.Model):
    hotel         = models.ForeignKey(Hotel, related_name='room_categories', verbose_name=_('hotel'))
    room_category = models.IntegerField(choices=profile_settings.HOTEL_CATEGORY_CHOICES, verbose_name=_('room category'))
    room_number   = models.CharField(max_length=255, blank=True, default='', verbose_name=_('room number'))
    price         = models.DecimalField(decimal_places=2, max_digits=7, verbose_name=_('price'))
    is_real_room  = models.BooleanField(default=True, help_text=_('Is real hotel room?'), verbose_name=_('is real?'))

    def __unicode__(self):
        return self.get_room_category_display()

    class Meta:
        app_label = 'profile'
        verbose_name = _('room category')
        verbose_name_plural = _('room categories')


class HotelRoomReserve(models.Model):
    room  = models.ForeignKey(HotelRoomCategory, related_name='hotel_reserves')
    claim = models.ForeignKey(Claim, related_name='hotel_reserves')
    arrival_date    = models.DateTimeField()
    departure_date  = models.DateTimeField()

    def __unicode__(self):
        return unicode(self.claim)

    class Meta:
        verbose_name = _('hotel room reserve')
        verbose_name_plural = _('hotel room reserves')

# --------------------------------------------------------------------------- #
#
#class Event(SortableModel):
#    title         = models.CharField(u'название', max_length=255)
#    title_en      = models.CharField(u'название (en)',max_length=255)
#    event_type    = models.IntegerField(u'тип события', blank=True, null=True, choices=profile_settings.EVENT_TYPE_CHOICES)
#    date_started  = models.DateTimeField(u'дата начала', db_index=True)
#    date_finished = models.DateTimeField(u'дата окончания', db_index=True)
#    annotation      = models.TextField(u'аннотация', blank=True, default='')
#    annotation_en   = models.TextField(u'аннотация (en)',blank=True, default='')
#    description     = models.TextField(u'описание', blank=True, default='')
#    description_en  = models.TextField(u'описание (en)', blank=True, default='')
#    place           = models.TextField(u'место проведения', blank=True, default='')
#    place_en        = models.TextField(u'место проведения (en)', blank=True, default='')
#    can_register    = models.BooleanField(u'возможность регистрации', default=True, db_index=True)
#    broadcast_url   = models.CharField(u'поток', max_length=255, null=True, blank=True)
#    is_displayable  = models.BooleanField(u'отображать?', default=False, db_index=True)
#    def __unicode__(self):
#        return self.title
#
#    class Meta:
#        verbose_name = _('event')
#        verbose_name_plural = _('events')
#        app_label = 'profile'
#        ordering = ['date_started', 'sort_order']
#
#class Events(CMSPlugin):
#    template = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('template'))
#    title    = models.CharField(max_length=255, blank=True, default='', verbose_name=_('title'))
#    date     = models.DateField(max_length=255, verbose_name=_('date'))
#
## --------------------------------------------------------------------------- #
#
#class EventsNow(CMSPlugin):
#    """Plugin persistent model for events tracking on index page"""
#    template = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('template'))
#    title    = models.CharField(max_length=255, blank=True, default='', verbose_name=_('title'))
## --------------------------------------------------------------------------- #
#
#class ClaimEvent(models.Model):
#    claim = models.ForeignKey(Claim, related_name='claim_events')
#    event = models.ForeignKey(Event, related_name='claim_events')
#
#    def __unicode__(self):
#        return u'%(claim)s -> %(event)s' % dict(
#            claim = self.claim,
#            event = self.event,
#        )
#
#    class Meta:
#        app_label = 'profile'
#        verbose_name = _('claim event')
#        verbose_name_plural = _('claim events')
#
