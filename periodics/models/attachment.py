# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from publisher.models import Publisher


class Attachment(Publisher):
    title      = models.CharField(max_length=255, )
    created_at = models.DateTimeField(auto_now=True, blank=True, db_index=True)
    file = models.FileField(upload_to='uploads/attachment')
    post = models.ForeignKey('periodics.Post', related_name='attachments')

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'periodics'
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')

