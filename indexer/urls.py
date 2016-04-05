from django.conf.urls.defaults import patterns, url
from views import ForumSearchView, forum_search_view_factory


from haystack.forms import HighlightedSearchForm

urlpatterns = patterns('indexer.views',
    url(
        regex = r'^like/(?P<ct>\w+)/(?P<id>\d+)/(?P<similar_type>\w+)/$',
        view  = 'similar',
        name  = 'similar_materials'
    ),
    url(
        regex = '^tag/(?P<ct>\w+)/(?P<tag>.+)/$',
        view  = 'tags_list',
        name  = 'tags_list_ct',
    ),
    url(
        regex = '^tag/(?P<tag>.+)/$',
        view  = 'tags_list',
        name  = 'tags_list',
    ),
)

urlpatterns += patterns('haystack.views',
    url(
        regex = r'^$',
        view  = forum_search_view_factory(
                    view_class=ForumSearchView,
                    template='indexer/search.html',
                    form_class=HighlightedSearchForm,
                ),
        name='haystack_search'),

    url(
        regex = r'^(?P<ct>\w+)/$',
        view  = forum_search_view_factory(
                    view_class=ForumSearchView,
                    template='indexer/search.html',
                    form_class=HighlightedSearchForm,
                ),
        name='haystack_search_ct'),
)
