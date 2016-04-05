# -*- coding: utf-8 -*-
from annoying.decorators import render_to
from cms.utils import get_language_from_request, get_page_from_request
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404
from library.models import Person

def get_category_from_request(request, use_session=True):
    """Get category for post at current cms page
    """
    try:
        key = request.session.get('referer', 'page_path')
        if use_session:
            request.path = request.session[key]
        page = get_page_from_request(request)
    except KeyError:
            raise Http404('You are behind django-cms')
    language = get_language_from_request(request)
    cms_category_plugins = page.cmsplugin_set.filter(
        Q(language=language) &
        Q(plugin_type__exact='PersonListOnPagePlugin')
    )
    if not cms_category_plugins.count():
        raise Http404('Category not found')
    return cms_category_plugins[0].personsincategory.category


@render_to()
def show(request, pk, person_slug):
    request.session['page_path'] = request.path
    category = get_category_from_request(request)
    person = get_object_or_404(Person, pk=pk, slug=person_slug)
    persons = Person.objects.filter(category__in = person.category.all()).distinct()
    tags = [t.strip() for t in person.tags.split(',') if t.strip() ]
    return {
        'category': category,
        'person'  : person,
        'persons' : persons.exclude(pk = person.pk),
        'persons_with_current': persons,
        'view_title': person.name,
        'tags': tags,
        'TEMPLATE': category.template,
    }
