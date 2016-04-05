# -*- mode: python -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _

class PeriodicsBase(models.Model):
    """Abstrac model for periodics core
    """
    created_by      = models.CharField(_('Creator'), max_length = 255)
    modified_by     = models.CharField(_('Modifier'), default = "script", max_length = 255, null = True, blank = True)
    created_at      = models.DateTimeField(_('Created at'), default=datetime.now)
    modified_at     = models.DateTimeField(_('Modified at'), auto_now = True)


    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_by = self.modified_by
        return super(PeriodicsBase, self).save(*args, **kwargs)


    class Meta:
        app_label = 'periodics'
        abstract = True

