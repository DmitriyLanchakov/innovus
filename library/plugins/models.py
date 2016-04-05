from cms.models.pluginmodel import CMSPlugin
from django.conf import settings
from django.db import models
from django.utils.text import ugettext_lazy as _
from library.models import Category

SORT_CHOICES = (
    (1, _("alphabet")),
    (2, _("preset")),
)

class PersonsList(CMSPlugin):
    # db_table 'cmsplugin_personslist'
    block_title = models.CharField(_('block title'), max_length=255, null=True, blank=True)
    sorting = models.IntegerField(_('sorting'), choices=SORT_CHOICES, default=2)
    per_page = models.IntegerField(_('persons count in list'), default=4)
    template = models.CharField(_('persons list template'), max_length=255, choices=settings.PERSONS_LIST_TEMPLATES)
    categories = models.ManyToManyField(
        Category,
        related_name='persons_plugin_categories',
    )


class PersonsInCategory(CMSPlugin):
    # db_table 'cmsplugin_personsincategory'
    block_title = models.CharField(_('block title'), max_length=255, null=True, blank=True)
    sorting = models.IntegerField(_('sorting'), choices=SORT_CHOICES, default=2)
    per_page             = models.IntegerField(_('persons count in list'), default=4)
    template             = models.CharField(
        verbose_name = _('persons list template'),
        max_length   = 255,
        choices      = settings.PERSONS_LIST_TEMPLATES,
    )
    category = models.ForeignKey(Category, related_name='lists')


class PersonsOnIndex(CMSPlugin):
    # db_table 'cmsplugin_personsonindex'
    sorting = models.IntegerField(_('sorting'), choices=SORT_CHOICES, default=2)
    speakers   = models.ForeignKey(Category, verbose_name=_('speakers'), related_name='speakers')
    speakers_count = models.IntegerField(_('speakers in list'), default=3)
    interviews = models.ForeignKey(Category, verbose_name=_('interviews'), related_name='interviews')
    interviews_count = models.IntegerField(_('interviews in list'), default=4)

    template             = models.CharField(
        verbose_name = _('persons list template'),
        max_length   = 255,
        choices      = settings.PERSONS_LIST_TEMPLATES,
    )


class Resources(CMSPlugin):
    # db_table 'cmsplugin_resources'
    count    = models.IntegerField()
    template = models.CharField(max_length=255,default='plugins/resources.html')
    title    = models.CharField(max_length=255, null=True, blank=True)
    categories = models.ManyToManyField(
        Category,
        related_name='resources_plugin_categories',
    )

    class Meta:
        app_label = 'cms'

