from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _



class SearchApp(CMSApp):
    name = _("Search app")
    urls = ["indexer.urls",]

apphook_pool.register(SearchApp)

