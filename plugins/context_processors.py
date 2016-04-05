from datetime import datetime
from cms.utils import get_page_from_request
from annoying.functions import get_config

def page_ancestors(request):
    page = get_page_from_request(request)
    ancestors_list = list()
    if page:
        ancestors_list = [ ance.reverse_id for ance in page.get_ancestors() if ance.reverse_id ]

    return { 'page_ancestors': ancestors_list }


def forum_period(request):
    today = datetime.today()
    
    return {
        'REG_START' : get_config('REG_START', today),
        'REG_END': get_config('REG_END', today),
        'NOW': today,
    }
