# coding: utf-8
from cms.models import Page
from django.db import models
from django.utils.translation import ugettext_lazy as _
from annoying.models import TimestampModel
from library.models import Category as PersonCategory
from openteam.models import NameModel
from publisher_admin.models import LanguageModel, CommentableModel
from events import settings as events_settings
from events.managers import ForumManager, ForumEventManager
from events.utils import get_namedtuple_choices


class Forum(NameModel, TimestampModel):
    is_current = models.BooleanField(_('is current?'),
                                 default=False,
                                 unique=True)
    starts_on  = models.DateField(_('event starts on'))
    ends_on    = models.DateField(_('event ends on'))

    objects = ForumManager()

    def __unicode__(self):
        return self.name


class ForumEvent(TimestampModel, CommentableModel):
    PROGRAM_TYPES = get_namedtuple_choices('PROGRAM_TYPES', (
        (0, 'general', _('business')),
        (1, 'youth', _('youth')),
        (2, 'cultural', _('cultural')),
        (3, 'satellite', _('satellite')),
        (4, 'master_business', _('master class')),
    ))

    forum       = models.ForeignKey(Forum, verbose_name=_('forum connection'), related_name='events')
    programm_type = models.PositiveIntegerField(_('programm type'),
            choices=PROGRAM_TYPES.get_choices(), default=PROGRAM_TYPES.general)
    title_color = models.CharField(_('title color'),
                                max_length=255,
                                default='blue',
                                choices=events_settings.EVENTS_COLORS_CLASSES)
    starts_on   = models.DateTimeField(_('event starts on'))
    ends_on     = models.DateTimeField(_('event ends on'))
    can_register_youth = models.BooleanField(_('can register youth'), default=False)
    can_register_business = models.BooleanField(_('can register business'), default=False)
    videostream = models.CharField(_('videostream URL'), max_length=512,
            null=True, blank=True)
    broadcast_start = models.DateTimeField(_('broadcast start'), blank=True,
            null=True)
    broadcast_end = models.DateTimeField(_('broadcast end'), blank=True,
            null=True)

    objects = ForumEventManager()

    class Meta:
        ordering = ['starts_on']

    @property
    def publisher_public(self):
        return self

    @property
    def comments_allow(self):
        return True

    @property
    def comments_premoderate(self):
        return False

    @property
    def participants(self):
        return self.registered.exclude(claim_state__in = [4, 5]).order_by('last_name')

    @property
    def participants_count(self):
        return self.participants.count()


def populate_broadcast_datetime(sender, **kwargs):
    instance = kwargs['instance']

    if instance.broadcast_start is None:
        instance.broadcast_start = instance.starts_on

    if instance.broadcast_end is None:
        instance.broadcast_end = instance.ends_on

models.signals.pre_save.connect(populate_broadcast_datetime, sender=ForumEvent)



class ForumEventContent(NameModel, LanguageModel):
    event = models.ForeignKey(ForumEvent, related_name='event_contents')
    display = models.BooleanField(_('display on site'), default=False)
    place = models.CharField(_('place'), max_length=512, blank=True)
    leader_name = models.CharField(_('leader name'), max_length=256, null=True, blank=True)
    moderators  = models.ForeignKey(PersonCategory, related_name='forum_events',
                    blank=True, null=True, verbose_name=_('moderators'))
    cms_page    = models.ForeignKey(Page, null=True, blank=True, verbose_name=_('cms page'))

    @property
    def page(self):
        return self.cms_page

