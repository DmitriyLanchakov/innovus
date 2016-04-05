# -*- coding: utf-8 -*-
'''
Created on 14.04.2010

@author: nimnull
'''
import string
from cms.utils import get_language_from_request

from django.db import models
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from annoying.decorators import render_to

from haystack.query import SearchQuerySet
from haystack.views import SearchView


DJANGO_TYPES = [
    'library.person',
    'text.text',
    'periodics.post',
    'library.video',
    'library.audio',
    'library.document',
    'library.picture',

]
#
#def prepare_search_types(types):
#    if 'text.text' in types:
#        types.remove('text.text')
#    return types


def process_solr_response(sqs, ct_list, source_id=None):
    response = list()

    for t in ct_list:
        ids = [ item.pk for item in sqs.filter_and(django_ct=t) if item.pk != source_id ]
        app_label, model = t.split('.')
        model_class =  models.get_model(app_label, model)
        model_set = model_class.objects.public().filter(pk__in = ids)

        response.append([string.replace(t, '.', '_'), model_set])

    return response


@render_to('indexer/search.html')
def similar(request, ct, id, similar_type):
    app_label, model = ct.split('_')
    model_class =  models.get_model(app_label, model)
    language = get_language_from_request(request)
    model = get_object_or_404(model_class, id=id)
    tags = [tag.strip() for tag in model.tags.split(',')]
    sqs = SearchQuerySet().filter(tags__in=tags).exclude(django_id = model.pk)
    response = generic_search(language, sqs, similar_type, exclude_text=True)
    title = {'en': 'Found for tags %s:',
             'ru': u'С метками %s найдено:',}
    response.update({
        'view_title': title[language] % ",".join([ tag for tag in tags ]),
        'model_id':id,
        'model_ct': ct
    })
    return response

def generic_search(language, sqs_generic, ct=None, exclude_text=False):
    ct = string.replace(ct or 'library.person', '_', '.')
    sqs_ct = sqs_generic.filter(language=language)
    if ct:
        sqs_ct = sqs_ct.filter(django_ct=ct)
    sqs_facet = sqs_generic.facet('django_ct')
    if exclude_text:
        sqs_facet = sqs_facet.exclude(django_ct='text.text')
    facet =  sqs_facet.facet_counts().get('fields', {'django_ct': ()})['django_ct']
    facet_filtered = dict(filter(lambda x: x[1] > 0, facet))
    facet = dict(facet)
    try:
        selected = ct if ct in facet_filtered else facet_filtered.keys()[0]
        sqs_ct = sqs_generic.filter(django_ct = selected)
    except IndexError:
        selected = None
    facets_ordered = [[key, facet.get(key, 0)] for key in DJANGO_TYPES]
    return {
        'facets': facets_ordered,
        'response': sqs_ct,
        'selected': selected,
    }

@render_to('indexer/search.html')
def tags_list(request,ct=None, tag=None):
    language = get_language_from_request(request)
    tag = tag or request.GET.get('tag', None)
    sqs_generic = SearchQuerySet().filter(tags=tag).order_by('-date')
    title = {'en': 'Found by tag &laquo;%(tag)s&raquo;:',
             'ru': u'С меткой &laquo;%(tag)s&raquo; найдено:',}
    response = generic_search(language, sqs_generic, ct, exclude_text=True)
    response.update({'tag': tag, 'view_title': title[language] % { 'tag': tag }})
    return response


class ForumSearchView(SearchView):

    def __init__(self, *args, **kwargs):
        self.content_type = kwargs.pop('ct') or 'library_person'
        super(ForumSearchView, self).__init__(*args, **kwargs)

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        language = get_language_from_request(self.request)
        sqs_generic = self.get_results()
        response = generic_search(language, sqs_generic, self.content_type)
        response.update({
            'form': self.form,
            'search_query': self.query,
            'view_title': _('Search results'),
        })
        return render_to_response(self.template, response, RequestContext(self.request))

def forum_search_view_factory(view_class=ForumSearchView, *args, **kwargs):
    def search_view(request, ct=None):
        kwargs.update({'ct': ct})
        return view_class(*args, **kwargs)(request)
    return search_view

