from datetime import datetime
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from library import FMT_VID, FMT_IMG, FMT_AUD, FMT_DOC
from library.managers import VideoManager, AudioManager, DocumentManager, PictureManager
from indexer.models import TaggedModel
from os.path import splitext
from publisher_admin.models import SortableModel, CommentableModel
from .base import Category


TYPE_CHOICES = (
    (FMT_VID, _('Video')),
    (FMT_AUD, _('Audio')),
    (FMT_IMG, _('Picture')),
    (FMT_DOC, _('Document')),
)


def upload_file(instance, filename):
    return settings.UPLOAD_RESOURCE_PATH + filename


def upload_snapshot(instance, filename):
    return settings.UPLOAD_RESOURCE_PATH + filename


class Resource(CommentableModel, SortableModel, TaggedModel):
    title = models.CharField(max_length=255)
    slug  = models.SlugField()
    file  = models.FileField(upload_to=upload_file)
    type  = models.IntegerField(choices=TYPE_CHOICES, editable=False)
    description  = models.TextField(blank=True, default='')
    date_created = models.DateTimeField(default=datetime.now(), editable=False)
    category     = models.ManyToManyField(Category, related_name='resources')
    snapshot = models.ImageField(
        blank     = True,
        null      = True,
        upload_to = upload_snapshot,
        help_text = _('Snapshot for resource, not required'),
    )
    _num = None

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.get_type() is not None:
            self.type = self.get_type()
        return super(Resource, self).save(*args, **kwargs)

    def extension(self):
        return splitext(self.file.path)[1].strip('.')

    def get_type(self):
        return self._num

    def set_position(self, category_id, order):
        position = self.positions.get(category__id=category_id)
        position.sort_order = order
        position.save()

    class Meta:
        app_label = 'library'
        ordering = ["-date_created"]
        verbose_name = _('resource')
        verbose_name_plural = _('resources')

    class PublisherMeta:
        exclude_fields_append = ['type', ]


class Video(Resource):
    objects = VideoManager()

    def get_type(self):
        return FMT_VID

    class Meta:
        app_label = 'library'
        verbose_name = _('video')
        verbose_name_plural = _('videos')
        proxy = True


class Audio(Resource):
    objects = AudioManager()

    def get_type(self):
        return FMT_AUD

    class Meta:
        app_label = 'library'
        verbose_name = _('audio')
        verbose_name_plural = _('audio')
        proxy = True


class Document(Resource):
    objects = DocumentManager()

    def get_type(self):
        return FMT_DOC

    class Meta:
        app_label = 'library'
        verbose_name = _('document')
        verbose_name_plural = _('documents')
        proxy = True


class Picture(Resource):
    objects = PictureManager()

    def get_type(self):
        return FMT_IMG

    class Meta:
        app_label = 'library'
        verbose_name = _('picture')
        verbose_name_plural = _('pictures')
        proxy = True


class ResourceToCategory(models.Model):
    related_model = models.ForeignKey(Resource, related_name='positions', db_column='resource_id')
    category = models.ForeignKey(Category)
    sort_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'library_resource_category'

    def resource(self):
        return self.related_model


