# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils import html
from haystack.indexes import *
import re

categories = getattr(settings, 'INDEXER_PERSON_CATEGORIES', (186, 187))

class PersonIndex(RealTimeSearchIndex):
    name        = CharField(model_attr='name')
    position    = CharField(model_attr='position')
    announce    = CharField(model_attr='announce')
    content     = CharField(document=True)
    language    = CharField(model_attr='language')
    categories  = MultiValueField()
    url         = CharField()
    tags        = MultiValueField()

    def prepare_categories(self, obj):
        return [ cat.id for cat in obj.category.all() ]

    def prepare_name(self, obj):
        return re.sub('<[^>]*>','',obj.name)

    def prepare_position(self, obj):
        return re.sub('<[^>]*>','',obj.position)

    def prepare_announce(self, obj):
        return re.sub('<[^>]*>','',obj.announce)

    def prepare_content(self, obj):
        prepared_content = re.sub('<[^>]*>','',obj.content)
        return " ".join([ prepared_content, obj.tags, obj.name ])

    def prepare_tags(self, obj):
        taglist =  obj.tags.split(', ')
        tags = [ html.escape(tag.strip('"')) for tag in taglist ]
        return tags

    def prepare_language(self, obj):
        return obj.language

    def prepare_url(self, obj):
        return obj.get_absolute_url()


    def get_queryset(self):
        return self.model.objects.all() #.filter(category__in=categories)

