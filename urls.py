from cms.sitemaps import CMSSitemap
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from periodics.feeds import CategoryRss
from library.feeds import PersonRss
from manage import rel


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin/',   include(admin.site.urls)),
    (r'^ajax/', include('ajax.urls')),
    (r'^periodics-admin/', include('admin.urls')),
    (r'^profile/', include('profile.urls')),
    (r'^rosetta/', include('rosetta.urls')),
#    url(
#        regex = '^programm/print/',
#        view  = 'profile.views.events.list_events_print',
#        name  = 'list_events_print',
#    ),
    url(r'^rss/periodics/(?P<sequence>\w+)/$', CategoryRss(), name='periodics_rss'),
    url(r'^rss/persons/$', PersonRss(), name='persons_rss'),
#    url(
#        regex = '^history/',
#        view  = include('library.urls'),
#    ),
    url(r'^comment/add/$', 'periodics.views.posts.add_comment', name='comment-add'),
    url(r'^comment/reply/(?P<parent_id>\d+)/$',
        'periodics.views.posts.add_comment', name='comment-reply'),

    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'cmspages': CMSSitemap}}),
    (r'^robots.txt$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'path': "robots.txt"}),
    (r'^favicon.ico$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'path': "favicon.ico"}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': rel('media'), 'show_indexes': True}),

    )

# django-cms endpoint
urlpatterns += patterns('',
    url(r'^', include('cms.urls')),
)


