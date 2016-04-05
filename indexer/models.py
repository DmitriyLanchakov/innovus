from django.db import models
from django.utils.translation import ugettext_lazy as _


class TaggedModel(models.Model):
    tags = models.CharField(
        max_length = 1024,
        verbose_name = _('Tags'),
        help_text    = _('List of all tags related to the item'),
        blank        = True,
        null         = True,
    )

    class Meta:
        abstract = True

