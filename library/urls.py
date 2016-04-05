# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('library.views.persons',
   url(
       regex = r'^(?P<pk>\d+)-(?P<person_slug>.*)/$',
       view  = 'show',
       name  = 'person',
   ),
)

