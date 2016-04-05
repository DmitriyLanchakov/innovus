from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _



class ForumEventsApp(CMSApp):
    name = _("Forum events app")
    urls = ["events.urls",]

apphook_pool.register(ForumEventsApp)

