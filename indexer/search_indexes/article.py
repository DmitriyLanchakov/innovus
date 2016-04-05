# -*- coding: utf-8 -*-
import re
from django.utils import html
from haystack.indexes import *
from indexer.utils import get_category_ids


class ArticleIndex(RealTimeSearchIndex):
    title       = CharField(model_attr='title')
#    annotation  = CharField(model_attr='annotation')
    content     = CharField(document=True)
    date        = DateTimeField(model_attr='date')
    language    = CharField()
    url         = CharField()
    categories  = MultiValueField()
    tags        = MultiValueField()


    def prepare_title(self, obj):
        return re.sub('<[^>]*>','',obj.title)

    def prepare_tags(self, obj):
        taglist =  obj.tags.split(', ')
        tags = [ html.escape(tag.strip('"')) for tag in taglist ]
        return tags

    def prepare_content(self, obj):
        prepared_content = re.sub('<[^>]*>','',obj.content)
        return " ".join([ prepared_content, obj.tags ])


    def prepare_language(self, obj):
        if obj.category.filter(pk__in = get_category_ids('ru')).count():
            return 'ru'
        elif obj.category.filter(pk__in = get_category_ids('en')).count():
            return 'en'


    def prepare_url(self, obj):
        return obj.get_absolute_url()


    def prepare_categories(self, obj):
        return [ cat.pk for cat in obj.category.all() ]


    def get_queryset(self):
        return self.model.objects.actual()

