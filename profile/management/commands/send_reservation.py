# -*- coding: utf-8 -*-
from django.conf import settings
from django.core import mail
from django.core.management.base import NoArgsCommand
from django.template import loader

from profile.models import HotelRoomReserve, CLAIM_SENT, \
    CLAIM_WAITING_APPROVEMENT, CLAIM_WAITING_PAYMENT, CLAIM_ACCEPTED

from openteam.utils import debug

HOTEL_CATEGORY_CHOICES = (
    'Аппартамент',
    'Люкс',
    'Студия',
    'Одноместный, первой категории',
    'Двухместный, первой категории',
    'Одноместный, второй категории',
    'Двухместный, второй категории',
)




class Command(NoArgsCommand):

    def handle_noargs(self, **opts):
        print self.email_hotel_reserved()


    def email_hotel_reserved(self):
        claim_reserves = HotelRoomReserve.objects.filter(claim__claim_state__in = [
            CLAIM_SENT,
            CLAIM_WAITING_APPROVEMENT,
            CLAIM_WAITING_PAYMENT,
            CLAIM_ACCEPTED,
        ])

        connection = mail.get_connection()
        messages = list()
        for reserve in claim_reserves:
            reserve.room_display = HOTEL_CATEGORY_CHOICES[reserve.room.room_category]
            email = reserve.claim.email if reserve.claim.user else reserve.claim.delegation_manager.email
            subject = loader.render_to_string('profile/email/reserve_added.subj.html',
                        {},
                    ),
            body = loader.render_to_string('profile/email/reserve_added.body.html',
                { 'claim': reserve.claim, 'reserve': reserve },
            ),
            messages.append(mail.EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [ '<%s>' % email ], connection=connection))



        for message in messages:
            try:
                message.send()
            except Exception, e:
                debug(e)



        return claim_reserves.count()

