from cms.models import CMSPlugin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from periodics.models import Category


class PageCategory(CMSPlugin):
    """
    """

    category = models.ForeignKey(Category,
        verbose_name=_('Category to display on page'),
        help_text=_('Select the category or create the new one'))

    is_commented    = models.BooleanField(_('Commented?'), default = True)
    is_moderated    = models.BooleanField(_('Moderated?'), default = False)
    per_page        = models.IntegerField(_('Per page'), default = 10)



    def save(self, *args, **kwargs):
        self.category.is_commented  = self.is_commented
        self.category.is_moderated  = self.is_moderated
        self.category.per_page      = self.per_page

        self.category.save()
        super(PageCategory, self).save(*args, **kwargs)



class LastPosts(CMSPlugin):
        categories  = models.ManyToManyField(Category,
                      verbose_name=_('Category to get posts from'),
                      help_text=_('Select the category or create the new one'))

        posts_count = models.IntegerField(_('Posts number to display'), default=5)

        template    = models.CharField(_('template'),
                                       max_length=255,
                                       choices=settings.PERIODICS_POST_LIST_TEMPLATES)

        @property
        def per_page(self):
            return self.posts_count


class LastComments(CMSPlugin):
    comments_count = models.IntegerField(_('Comments count to display'), default=10)



class LastVideo(CMSPlugin):
    category = models.ForeignKey(Category, verbose_name=_('Category with video'))

    __unicode__ = lambda self: self.category.title

    
class Innonews(CMSPlugin):
    world  = models.ForeignKey(Category, verbose_name=_("category 'in world'"), related_name='innonews_world')
    russia = models.ForeignKey(Category, verbose_name=_("category 'in russia'"), related_name='innonews_russia')
    tomsk  = models.ForeignKey(Category, verbose_name=_("category 'in tomsk'"), related_name='innonews_tomsk')
    template = models.CharField(_('template'), max_length=255, choices=settings.PERIODICS_INNONEWS_TEMPLATES)