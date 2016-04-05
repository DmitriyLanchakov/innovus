# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from publisher.manager import PublisherManager

class PostManager(PublisherManager):
    """
    Manager for Post model
    """



    def actual(self):
        Q, now = models.Q, datetime.now()
        return super(PostManager, self).get_query_set() .\
            filter(is_active=True)  .\
            filter(publisher_is_draft=False).\
            filter(Q(public_from__lte=now) | Q(public_from=None)) .\
            filter(Q(public_till__gt=now)  | Q(public_till=None)).\
            order_by('-public_from')


    def by_date(self, year=None, month=None, day=None):
        """
        Finds posts for given date or its fragments
        """
        queryset = self.get_query_set().order_by('-public_from')

        if year:
            queryset = queryset.filter(public_from__year=year)

        if month:
            queryset = queryset.filter(public_from__month=month)

        if day:
            queryset = queryset.filter(public_from__day=day)

        return queryset


class CommentQuerySet(models.query.QuerySet):

    def approved(self):
        return self.filter(is_approved=True)


class CommentManager(models.Manager):
    """
    Manager for Comment model
    """
    def get_query_set(self):
        return CommentQuerySet(self.model)

    def approved(self):
        return self.get_query_set().approved()


class CategoryManager(PublisherManager):

    def get_query_set(self):

        super_qs = super(CategoryManager, self).get_query_set()
        return super_qs.public()

