# encoding: utf-8
from annoying.models import TimestampModel
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from indexer.models import TaggedModel
from os.path import normpath, splitext
from publisher_admin.models import LanguageModel, CommentableModel
from .base import Category


def upload_to(instance, filename):
    return normpath(
        '%(path)s/%(name)s.%(ext)s' % dict(
            path = settings.UPLOAD_PHOTO_PATH,
            name = instance.slug,
            ext  = splitext(filename)[1].strip('.'),
        )
    )


class Person(LanguageModel, CommentableModel, TaggedModel, TimestampModel):
    name       = models.CharField(max_length=255, )
    slug       = models.SlugField()
    position   = models.TextField(blank=True)
    announce   = models.TextField(blank=True)
    content    = models.TextField(blank=True)
    photo      = models.ImageField(upload_to=upload_to)
    category = models.ManyToManyField(Category, related_name='persons')
    old_id     = models.PositiveIntegerField(null=True, blank=True)

    @property
    def comments_allow(self):
        return True

    @property
    def comments_premoderate(self):
        return True

    @property
    def publisher_public(self):
        return self

    def get_absolute_url(self):
        """resolve person url in django-cms context
        """
        from library.plugins.models import PersonsInCategory, PersonsList
        from events.models import ForumEventContent
        url = "%(pk)d-%(slug)s/" % { 'pk': self.pk, 'slug': self.slug }
        plugins_qs = [
            PersonsInCategory.objects.filter(category__in = self.category.all()),   #order matters
            PersonsList.objects.filter(categories__in = self.category.all()),
            ForumEventContent.objects.filter(moderators__in = self.category.all()),
        ]
        for i, qs in enumerate(plugins_qs):
            page = qs[0].page if qs.count() else None
            if page:
                url_prefix = page.get_absolute_url(language=qs[0].language)
                if i == 0:
                    return url_prefix + url
                return url_prefix
        return url

    def set_position(self, category_id, order):
        position = self.positions.get(category__id=category_id)
        position.sort_order = order
        position.save()

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'library'
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    class PublisherMeta:
        exclude_fields_append = ['sort_order', ]


class PersonToCategory(models.Model):
    category = models.ForeignKey(Category)
    related_model = models.ForeignKey(Person, related_name='positions', db_column='person_id')
    sort_order = models.IntegerField(default=0)

    class Meta:
        app_label = 'library'
        db_table = 'library_person_category'

    def person(self):
        return self.related_model
