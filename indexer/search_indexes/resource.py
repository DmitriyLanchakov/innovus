# -*- coding: utf-8 -*-
from django.utils import html

from haystack.indexes import *

import re


class ResourceIndex(RealTimeSearchIndex):
    title         = CharField(model_attr='title')
    content       = CharField(document=True)
    language      = CharField()
    tags          = MultiValueField()

    def prepare_content(self, obj):
        prepared_content = re.sub('<[^>]*>','',obj.description)
        return " ".join([ prepared_content, obj.tags, obj.title ])

    def prepare_tags(self, obj):
        taglist =  obj.tags.split(', ')
        tags = [ html.escape(tag.strip('"')) for tag in taglist ]
        return tags

    def prepare_language(self, obj):
        categories = obj.category.all()
        if categories.count():
            return categories[0].language
        else:
            return 'ru'


    def get_queryset(self):
        return self.model.objects.all()

