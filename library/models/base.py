from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from openteam.models import SortableModel
from publisher_admin.models import LanguageModel, CommentableModel


class Category(SortableModel, LanguageModel, CommentableModel):
    title = models.CharField(max_length=255)
    slug  = models.SlugField()
    old_person_id = models.PositiveIntegerField(null=True, blank=True)
    template = models.CharField(_('render template'), max_length=512, choices=settings.RESOURCES_TEMPLATES, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'library'
        verbose_name = _('category')
        verbose_name_plural = _('categories')

