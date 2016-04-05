# -*- coding: utf-8 -*-

from django.template import Node, Library

register = Library()

@register.inclusion_tag('admin/periodics/post/filter.html', takes_context=True)
def admin_list_filter_post(context, cl, spec):
    return {
        'filter'  : spec.field.name,
        'title'   : spec.title(),
        'choices' : list(spec.choices(cl)),
        'request' : context.get('request'),
    }


@register.inclusion_tag('admin/periodics/post/change_list_results.html')
def result_list_post(cl):
    return {
        'cl': cl,
        'result_headers': list(result_headers(cl)),
        'results':        list(results(cl))
    }

#admin_list_filter = register.inclusion_tag('admin/filter.html')(admin_list_filter)

@register.inclusion_tag('admin/periodics/post/submit_line.html', takes_context=True)
def submit_post_row(context):
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    return {
        'post': True,
        'onclick_attrib': (opts.get_ordered_objects() and change
                            and 'onclick="submitOrderForm();"' or ''),
        'show_delete_link': (not is_popup and context['has_delete_permission']
                              and (change or context['show_delete'])),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another': context['has_add_permission'] and
                            not is_popup and (not save_as or context['add']),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': True
    }

