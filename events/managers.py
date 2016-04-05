# encoding: utf-8
from django.db import models
from django.db.models import Q


class ForumManager(models.Manager):

    def current(self):
        return self.get_query_set().get(is_current=True)


class ForumEventQuerySet(models.query.QuerySet):

    def for_registration(self):
        return self.filter(Q(can_register_youth=True) | Q(can_register_business=True), forum__is_current=True)


class ForumEventManager(models.Manager):

    def get_query_set(self):
        return ForumEventQuerySet(self.model)

    def __getattr__(self, name, *args):
        if name.startswith('_'):
            raise AttributeError
        return getattr(self.get_query_set(), name, *args)

#    def for_registration(self):
#        return self.get_query_set().for_registration()
