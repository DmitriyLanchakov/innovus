from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class PersonsApp(CMSApp):
    name = _("Persons app")
    urls = ["library.urls",]

apphook_pool.register(PersonsApp)

