from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models.pluginmodel import CMSPlugin
from events.models import Forum, ForumEvent

class ForumProgramm(CMSPlugin):
    forum = models.ForeignKey(Forum, verbose_name=_('forum'))
    program_type = models.PositiveIntegerField(_('program_type'),
            choices=ForumEvent.PROGRAM_TYPES.get_choices())


class ForumHistory(CMSPlugin):
    forum = models.ForeignKey(Forum, verbose_name=_('forum'))


class Broadcast(CMSPlugin):
    forum = models.ForeignKey(Forum, verbose_name=_('forum'))
    channel_title = models.CharField(_('channel title'), max_length=512,
            blank=True)
    channel_stream = models.CharField(_('channel stream'), max_length=512,
            blank=True)
    channel_display = models.BooleanField(_('append to playlist?'),
            default=False)
