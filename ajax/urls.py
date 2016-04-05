# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('ajax.views',
    url(
        regex = '^news/(?P<sequence>\w+)/$',
        view  = 'last_news',
        name  = 'ajax_last_news',
    ),
#    url(
#        regex = '^persons/$',
#        view  = 'persons_list',
#        name  = 'ajax_persons_list',
#    ),
    url(
        regex = '^events/$',
        view  = 'events',
        name  = 'ajax_events',
    ),

    url(
        regex = '^hidden_text/(?P<id>\d+)/$',
        view  = 'load_hidden_text',
        name  = 'load_hidden_text',
    ),

    url(
        regex = '^archive_years/$',
        view  = 'render_archive_years',
        name  = 'render_archive_years',
    ),

)

