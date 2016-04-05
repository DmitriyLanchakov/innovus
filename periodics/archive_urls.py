from django.conf.urls.defaults import *



urlpatterns = patterns('periodics.views',
#-------------------------------------------------------------------------------
    url(
        regex   = r'^$',
        view    = 'posts.archive',
    ),
    url(
        regex   = r'^(?:(?P<year>\d{4})(?:/(?P<month>\d{1,2}))?)?/?$',
        view    = 'posts.by_date',
    ),
)

