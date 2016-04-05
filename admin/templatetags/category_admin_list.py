from django.template import Library
from django.contrib.admin.templatetags.admin_list import result_headers, results

register = Library()

def category_result_list(cl):
    return {
        'cl': cl,
        'result_headers': list(result_headers(cl)),
        'results': list(results(cl)),
    }
category_result_list = register.inclusion_tag("admin/periodics/category/change_list_results.html")(category_result_list)
