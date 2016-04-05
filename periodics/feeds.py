# -*- coding: utf-8 -*-
from cms.utils import get_language_from_request

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from periodics.models import Post, Category


class CategoryRss(Feed):
    feed_type = Rss201rev2Feed
#    description_template = 'periodics_rss.html'
    title_template = "rss_title.html"



    def title(self, obj):
        return _('Tomsk forum of innovations')


    def link(self, obj):
        return "/"


    def description(self, obj):
        if self.sequence == 'inno':
            return _('Innovation news')
        elif self.sequence == 'site':
            return _('New on site')


    def get_object(self, request, sequence):
        self.url_path = 'http://' + request.META['HTTP_HOST']
        self.sequence = sequence
        self.lang = get_language_from_request(request)
        return Category.objects.filter(pk__in = settings.NEWS_AGREGATE_CATEGORIES[self.lang][self.sequence])

#        category_plugins = PageCategory.objects.filter(page=self.page, language=self.lang).order_by('category__sort_order')
#        categories = [ plugin.category for plugin in category_plugins ]
#        return categories



    def items(self, obj):
        return Post.objects.actual().filter(category__in = obj).order_by('-public_from')[:10]


    def item_title(self, item):
        return mark_safe(item.title)


    def item_description(self, item):
        return mark_safe(item.annotation)


    def item_pubdate(self, item):
        return item.date


    def item_link(self, item):
        return self.url_path + item.get_absolute_url()

