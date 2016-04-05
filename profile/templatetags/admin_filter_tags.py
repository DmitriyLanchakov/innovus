# -*- coding: utf-8 -*-

from urlparse import parse_qs
from django.template import Library

# --------------------------------------------------------------------------- #

register = Library()

# --------------------------------------------------------------------------- #

@register.inclusion_tag('admin/profile/claim/filter.html')
def admin_list_filter(cl, spec):
    choices, options = list(spec.choices(cl)), list()
    field_name = spec.field.name

    for i in choices:
        parsed = parse_qs(i['query_string'].strip('?'))
        key = '%s__exact' % field_name


        i['parsed_query'] = parsed
        
        if key in parsed:
            i['option_value'] = parsed[key].pop()

    return dict(
        title      = spec.title(),
        field_name = field_name,
        choices    = choices,
        options    = options,
    )

