# -*- mode: python -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class BannedIp(models.Model):
    """
    Banned ip addresses storage
    """
    banned_by  = models.ForeignKey(User, verbose_name=_('Banned by'), related_name='ip_bans')
    banned_at  = models.DateTimeField(_('Ban date and time'), auto_now_add=True)
    ip_address = models.IPAddressField(_('Banned IP address'), unique=True)
    reason     = models.CharField(max_length=255, default='', blank=True)

    def __unicode__(self):
        return self.ip_address

    class Meta:
        app_label = 'periodics'
        verbose_name = _('Banned IP address')
        verbose_name_plural = _('Banned IP addresses')

