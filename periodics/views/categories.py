# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
from periodics.models import Category, Post

def filter(request, category_id):
    """
    """
    category = get_object_or_404(Category, pk=category_id)

    return object_list(request, **{
        'template_object_name' : 'posts',
        'queryset'      : Post.objects.public().filter(category=category),
        'template_name' : 'category_list.html',
        'extra_context' : {
            'category': category,
        }
    })