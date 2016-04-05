# -*- coding: utf-8 -*-
from haystack.indexes import *
import re


class TextIndex(RealTimeSearchIndex):
    title    = CharField()
    content  = CharField(document = True)
    language = CharField(model_attr = 'language')


    def prepare_content(self, obj):
        prepared_content = re.sub('<[^>]*>','',obj.body)
        return " ".join([ prepared_content, obj.page.get_title(language = obj.language) ])

    def prepare_title(self, object):
        return object.page.title_set.get(language = object.language).title


    def get_queryset(self):
        return self.model.objects.public()

