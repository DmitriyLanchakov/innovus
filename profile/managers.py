# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.query import QuerySet

from profile import settings as profile_settings

class ClaimQuerySet(QuerySet):

    def active(self):
        return self.exclude(claim_state__in=[ profile_settings.CLAIM_CANCELLED, profile_settings.CLAIM_REJECTED ])


    def not_tomsk(self):
        return self.exclude(region__id=profile_settings.TOMSK_REGION_ID)



    def tomsk(self):
        return self.filter(region__id=profile_settings.TOMSK_REGION_ID)


    def registered(self):
        return self.filter(is_registered=True)


    def unregistered(self):
        return self.filter(is_registered=False)



class ClaimManager(models.Manager):

    def get_query_set(self):
        return ClaimQuerySet(self.model)


    def active(self):
        return self.get_query_set().active()

