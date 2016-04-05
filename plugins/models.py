from cms.models import CMSPlugin
from cms.plugins.text.models import AbstractText
from django.utils.translation import ugettext_lazy as _
from django.db import models

class Toggle(AbstractText):
    title = models.CharField(_('title'), max_length=255)


class Menu(CMSPlugin):
    """
    render a nested list of all children of the pages
    - from_level: starting level
    - to_level: max level
    - extra_inactive: how many levels should be rendered of the not active tree?
    - extra_active: how deep should the children of the active node be rendered?
    - namespace: the namespace of the menu. if empty will use all namespaces
    - root_id: the id of the root node
    - template: template used to render the menu

    """
    from_level = models.PositiveIntegerField(_('starting level'), default=0)
    to_level = models.PositiveIntegerField(_('max level'), default=100)
    extra_inactive = models.PositiveIntegerField(
        verbose_name = _('extra inactive'),
        help_text = _('how many levels should be rendered of the not active tree?'),
        default=0
    )
    extra_active = models.PositiveIntegerField(
        verbose_name = _('extra active'),
        help_text = _('how deep should the children of the active node be rendered?'),
        default=100
    )
    root_id = models.CharField(
        verbose_name = _('root id'),
        help_text = _('reverse_id of the root page'),
        max_length=255,
        null=True,
        blank=True
    )
    template = models.CharField(
        verbose_name = _('template to render menu with'),
        max_length=255,
        default = 'menu/extralevel_navigation.html'
    )


class Sitemap(CMSPlugin):
    template = models.CharField(
            verbose_name = _("Template name"),
            max_length=255, 
            )
