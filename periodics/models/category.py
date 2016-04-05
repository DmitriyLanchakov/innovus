# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from periodics.models.base import PeriodicsBase
from periodics.managers import CategoryManager
from publisher.models import Publisher, PublisherManager
from publisher_admin.models import SortableModel, LanguageModel

class Category(PeriodicsBase, SortableModel, LanguageModel):
    """
    Post category model
    """

    title           = models.CharField(_('Title'), max_length = 255)
    is_commented    = models.BooleanField(_('Commented?'), default = True)
    is_moderated    = models.BooleanField(_('Moderated?'), default = False)
    per_page        = models.IntegerField(_('Per page'), default = 10)
    post_template   = models.CharField(_('template for post'), max_length='255',choices=settings.PERIODICS_POST_TEMPLATES, default = 'post-single.html')

    __unicode__ = lambda self: self.title

    publisher_state = 1

    class Meta:
        app_label = 'periodics'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

