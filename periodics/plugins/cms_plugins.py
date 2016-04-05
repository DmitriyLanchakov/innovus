# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from periodics.models import Post, Comment
from periodics.plugins.models import PageCategory, LastPosts, LastComments, LastVideo, Innonews

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool


class PageCategoryPlugin(CMSPluginBase):
    admin_preview = False
    model = PageCategory
    name = _("Category on page")
    render_template = "plugins/posts_in_category.html"

    def render(self, context, instance, placeholder):
        posts = Post.objects.actual().filter(category__in = [instance.category])

        context.update({
            'category':instance.category,
            'posts': posts,
            'object':instance,
            'placeholder':placeholder
        })

        return context

# ------------------------------------------------------------------------------

class LastPostsPlugin(CMSPluginBase):
    admin_preview = False
    model = LastPosts
    name = _("Last posts from category")
    render_template = settings.PERIODICS_POST_LIST_TEMPLATES[0][0]
    filter_horizontal = ('categories', )

    def render(self, context, instance, placeholder):
        posts = Post.objects.actual().filter(category__in = instance.categories.all()).order_by('-public_from')[:instance.posts_count]
        self.render_template = instance.template or LastPostsPlugin.render_template

        context.update({
            'event': posts[0],
            'posts': posts,
            'object':instance,
            'placeholder':placeholder,
            'next': Post.objects.public().filter(category__in=instance.categories.all()).count() > instance.posts_count,
        })

        return context


# ------------------------------------------------------------------------------

class LastCommentsPlugin(CMSPluginBase):
    admin_preview = False
    model = LastComments
    name = _('Latest comments feed')
    render_template = "recent_comments.html"


    def render(self, context, instance, placeholder):
        comments = Comment.objects.approved().order_by('-created_at')[:instance.comments_count]

        context.update({
            'comments': comments
        })
        return context


# -------------------------------------------------------------------------------
class LastVideoPlugin(CMSPluginBase):
    admin_preview = False
    model = LastVideo
    name = _('Latest video from post')
    render_template = "recent_video.html"


    def render(self, context, instance, placeholder):
        posts = instance.category.posts.actual().order_by('-public_from')
        post = posts[0] if posts.count() else None

        return context.update({
            'post': post,
            'placeholder': placeholder,
            'object': instance,
        })


class InnonewsPlugin(CMSPluginBase):
    admin_preview = False
    model = Innonews
    name  = _('Innonews')
    render_plugin = settings.PERIODICS_INNONEWS_TEMPLATES[0][0]

    def render(self, context, instance, placeholder):
        self.render_template = instance.template or self.render_template

        context.update({
            'world': Post.objects.actual().filter(category=instance.world)[:1],
            'russia': Post.objects.actual().filter(category=instance.russia)[:1],
            'tomsk': Post.objects.actual().filter(category=instance.tomsk)[:1],
            'object': instance,
            'placeholder': placeholder,
        })
        return context
    
plugin_pool.register_plugin(InnonewsPlugin)
plugin_pool.register_plugin(LastVideoPlugin)
plugin_pool.register_plugin(LastCommentsPlugin)
plugin_pool.register_plugin(LastPostsPlugin)
plugin_pool.register_plugin(PageCategoryPlugin)

