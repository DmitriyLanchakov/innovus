from cms.utils import get_page_from_request
from cms.utils.navigation import NavigationNode

from django.utils.translation import ugettext as _

from periodics.views.posts import get_category_from_request

def get_nodes(request):
    archive = NavigationNode(_('Archive'), 'archive/')
    res = [archive, ]

    return res
    
