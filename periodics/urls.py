from django.conf.urls.defaults import *



urlpatterns = patterns('periodics.views',
#-------------------------------------------------------------------------------
    url(
        regex   = r'^(?P<pk>\d+)-(?P<slug>.*)/$',
        view    = 'posts.show',
        name	= 'post-url',
    ),
#    url('^books/$', include('cms.urls')),
#-------------------------------------------------------------------------------
    url(
        regex   = r'^archive/$',
        view    = 'posts.archive',
    ),
    url(
        regex   = r'^archive/(?:(?P<year>\d{4})(?:/(?P<month>\d{1,2}))?)?/?$',
        view    = 'posts.by_date',
    ),
)

