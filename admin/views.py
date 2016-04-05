# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from openteam.decorators import staff_required
from annoying.decorators import ajax_request, render_to
from annoying.functions import get_object_or_None

from periodics.forms import PostAdminForm, CategoryAdminForm
from periodics.models import Category, Post

# --------------------------------------------------------------------------- #
@staff_required
@ajax_request
def update_category_order(request):
    """view to process jquery sortable in admin category list
    """
    categories = list(Category.objects.order_by('sort_order', 'id'))
    items = request.POST.getlist('item[]')

    for order in xrange(0,len(items)):
        i = int(items[order])
        categories[i].sort_order = order
        categories[i].save()

    return HttpResponse('All ok')


# ---------------------------------------------------------------------------- #

@staff_required
@ajax_request
def add_category(request, post_id=None):
    if request.method == 'POST':
        result = {}
        form = CategoryAdminForm(request.POST)

        if form.is_valid():
            category = form.save()
            post = get_object_or_None(Post, pk=post_id)

            if post:
                post.category.add(category)
                result['post'] = unicode(post)

            result['category'] = category

        else:
            result['errors'] = {}
            for k in form._errors:
                result['errors'][k] = unicode(form._errors[k])

        result['success'] = form.is_valid()
        return result

    else:
        return {'action' : request.path_info,
                'fields' : dict([(unicode(f.label), unicode(f)) for f in CategoryAdminForm()]),
        }

# --------------------------------------------------------------------------- #

@staff_required
@render_to('admin/periodics/post/includes/status.html')
def post_save(request):
    """
    Отображение для полного сохранения и опубликования статьи без
    перезагрузки страницы

    Не использует XMLHttpRequest, т.к. требуется работа с типом
    формы multipart/form-data и сохранением даты и времени.
    """
    result = {}

    if request.method == 'POST':
        try:
            object_id = int(request.POST.get('object_id'))
        except:
            object_id = 0

        instance  = get_object_or_None(Post, pk=object_id)
        form = PostAdminForm(request.POST, instance=instance)

        if form.is_valid():
            result['created'] = instance is None
            form.save()

        else:
            result['errors'] = []
            for k in form._errors:
                result['errors'].append({'field':k, 'errors': unicode(form._errors[k])})

        result['success'] = form.is_valid()

    return result

