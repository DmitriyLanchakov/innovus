# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.models import User

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import truncate_words
import mptt
from openteam.utils import html2text, send_email

from pytils import translit
from indexer.models import TaggedModel
from publisher.models import Publisher
from publisher.manager import PublisherManager
from photologue.models import Gallery

from periodics.managers import PostManager, CommentManager
from periodics.models.category import Category
from periodics.models.base import PeriodicsBase


COMMENT_SETTINGS_CHOICES = (
   ('',  _('Use category settings')),
   (True,  _('Allow')),
   (False, _('Deny')),
)

PREMODERATE_SETTINGS_CHOICES = (
   ('',  _('Use category settings')),
   (True,  _('Enable')),
   (False, _('Disable')),
)



class Comment(PeriodicsBase):
    """Comment model
    """
    author_name  = models.CharField(verbose_name=_('Name'), max_length=255, default='')
    author_email = models.EmailField(verbose_name=_('Email'), max_length=255, default='')
    user = models.ForeignKey(User, related_name='comments', blank=True, null=True)

    parent      = models.ForeignKey('self', null = True, blank = True, related_name = 'children')
    content     = models.TextField(_('Content'))
    ip_address  = models.IPAddressField(_('IP Address'))
    is_approved = models.BooleanField(default=True, db_index=True)

    publisher_state = 0

    _commentable_content_type = models.ForeignKey(ContentType, related_name="posts_comments")
    _commentable_object_id = models.PositiveIntegerField()

    commentable = generic.GenericForeignKey(ct_field="_commentable_content_type", fk_field="_commentable_object_id")

    objects = CommentManager()
    admin_objects = models.Manager()

    def approve(self):
        self.is_approved = True
        self.save()

    def __unicode__(self):
        return self.content

    @property
    def clean_content(self):
        return truncate_words(html2text(self.content), 70)

    class Meta:
        app_label = 'periodics'
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

if Comment not in mptt.registry:
    mptt.register(Comment, )


def comment_created_notification(sender, **kwargs):
    if kwargs['created']:
        send_email(
            to      = 'innovus@tomskforum.ru',
            tpl     = 'comment_posted',
            context = {'comment': kwargs['instance'], 'text': html2text(kwargs['instance'].content) },
        )

models.signals.post_save.connect(comment_created_notification, sender=Comment)



class Post(Publisher, PeriodicsBase, TaggedModel):
    """
    Post model
    """
    title        = models.CharField(max_length=255, )
    slug         = models.SlugField(max_length=255, help_text=_('SEO friendly post title'))
    annotation   = models.TextField(default='', blank=True)
    content      = models.TextField(default='', blank=True)
    public_from  = models.DateTimeField(blank=True, null=True)
    public_till  = models.DateTimeField(blank=True, null=True)
    is_active    = models.BooleanField(default=True, verbose_name=_('Show on site'))

    picture_src   = models.ImageField(upload_to='uploads/images', blank=True, null=True)
    picture_show  = models.BooleanField(default=False, help_text=_('Show picture on Post page'))
    picture_alt   = models.CharField(max_length=255, blank=True, default='')
    picture_title = models.CharField(max_length=255, blank=True, default='')


    comments_allow       = models.NullBooleanField(blank=True, null=True, choices=COMMENT_SETTINGS_CHOICES, default=None, verbose_name=_('Allow comments'), help_text=_('This Post settings overrides same Category settings'))
    comments_premoderate = models.NullBooleanField(blank=True, null=True, choices=PREMODERATE_SETTINGS_CHOICES, default=None, verbose_name=_('Premoderate comments'), help_text=_('This Post settings overrides same Category settings'))

    comments = generic.GenericRelation(Comment,
        object_id_field="_commentable_object_id",
        content_type_field="_commentable_content_type"
    )

    category     = models.ManyToManyField(Category, related_name='posts')

    old_blogpost_id = models.IntegerField(blank=True,null=True,unique=True)


    objects = PostManager()
    admin_objects = PublisherManager()

    gallery = models.ForeignKey(Gallery, blank=True, null=True, related_name='posts')



    @property
    def date(self):
        """
        Returns actual date of news: if ``public_from`` is not None it will
        be used, ``created_add`` will be used otherwise
        """
        return self.public_from if self.public_from else self.created_at


    def get_absolute_url(self):
        """resolve post url in django-cms context
        """
        url = "%(pk)d-%(slug)s/" % { 'pk': self.pk, 'slug': self.slug }
        try:
            from periodics.plugins.cms_plugins import PageCategory
        except ImportError:
            return url

        category_plugins = PageCategory.objects.filter(category__in = self.category.all())

        page = category_plugins[0].page if category_plugins.count() else None

        if page:
            url = page.get_absolute_url(language=category_plugins[0].language) + url

        return url


    @property
    def is_scheduled(self):
        return self.public_from > datetime.now() if self.public_from else False


    @property
    def is_expired(self):
        return self.public_till < datetime.now() if self.public_till else False


    @property
    def picture(self):
        """
        Returns picture on Post page if ``show`` flag is *ON*
        """

        if self.picture_src and self.picture_show:
            return self.picture_show
        return None


    def save(self,commit=False, **kwargs):
        """
        Overrides standart save() method
        """
        #public start time should always be lesser than public end time
        if self.public_from and self.public_till and self.public_till <= self.public_from:
            raise exceptions.ValidationError(_("Expired date is less than published date"))
        #if we have new instance, then default for public start time sets equals
        #to creation time cause this field is required by periodics logic
        if not self.pk:
            self.created_by = self.modified_by

            if not self.public_from:
                self.public_from = self.created_at

        return super(Post, self).save(**kwargs)


    def __unicode__(self):
        return self.title


    class Meta:
        ordering = ["-public_from"]
        app_label = 'periodics'


    class PublisherMeta:
        exclude_fields_append = ['old_blogpost_id',]


def populate_slug(sender, **kwargs):
    post = kwargs['instance']
    post.slug = translit.slugify(truncate_words(post.title, num=3, end_text=''))


def check_public_from_date(sender, **kwargs):
    post = kwargs['instance']
    post.public_from = post.public_from or post.created_at


def delete_public_post(sender, **kwargs):
    posts2delete = Post.objects.public().filter(publisher_draft = None)
    posts2delete.delete()


models.signals.pre_save.connect(populate_slug, sender=Post)
models.signals.pre_save.connect(check_public_from_date, sender=Post)
models.signals.post_delete.connect(delete_public_post, sender=Post)

