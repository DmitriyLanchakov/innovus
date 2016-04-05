from django.conf import settings
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.text import ugettext_lazy as _

from publisher_admin.admin import SortableAdmin

from library.models import *


class BaseModelAdmin(admin.ModelAdmin):
    prepopulated_fields = dict(
        slug = ['title',]
    )


class ResourceAdmin(BaseModelAdmin, SortableAdmin):
    actions_on_top = False
    list_display = (
        'title', 'date_created',
    )
    list_filter = ('category', )
    search_fields = ('title',  'tags', 'description')
    filter_horizontal = ('category', )
    change_list_template = "admin/library/resource/change_list.html"
    fieldsets = (
        (None, {'fields': ['title', 'slug', 'description', 'tags']}),
        (_('Files'), {'fields': ['file', 'snapshot']}),
        (_('Categories'), {'fields': ['category']}),
    )

    class Media:
        css = {
            'screen': (
                settings.CSS_URL + 'admin/inline_form.css',
                settings.CSS_URL + 'smoothness/jquery-ui-1.8.11.custom.css',
                settings.CSS_URL + 'admin/history-dropdown.css'
            )
        }
        js = (
            settings.JS_URL + 'admin/history-dropdown.js',
        )
    def response_change(self, request, obj):
        """
        Overrides a standart 'change' response object for resource admin to
        avoid proxy model problems
        """
        origin = super(ResourceAdmin, self).response_change(request, obj)

        if request.POST.get('_publish', None):
            resource = get_object_or_404(Resource, pk=obj.id)
            resource.tags = obj.tags
            resource.save()
            resource.publish()

        return origin

    def response_add(self, request, obj, post_url_continue='../%s/'):
        """
        Overrides a standart 'add' publisher response for resource admin
        to avoid proxt model problem
        """
        origin = super(ResourceAdmin, self).response_add(request, obj,
            post_url_continue
        )

        if request.POST.get('_publish'):
            resource = get_object_or_404(Resource, pk=obj.id)
            resource.tags = obj.tags
            resource.save()
            resource.publish()

        return origin

    def action_publish(self, request, queryset):
        """
        Override publish action to avoid proxy model problem
        """
        super(ResourceAdmin, self).action_publish(request, queryset)

        sets = dict()
        for q in queryset:
            sets[q.id] = q

        for q in Resource.objects.filter(pk__in=sets.keys()):
            q.tags = sets[q.id].tags
            q.save()
            q.publish()


class CategoryAdmin(SortableAdmin, BaseModelAdmin):
    list_display = (
        'title', 'display_page', 'display_count', 'is_commented',
        'is_moderated',
    )
    list_filter  = ('language', 'is_commented', 'is_moderated', )
    ordering     = ('sort_order', )
    fieldsets = (
        (None, 
            {'fields': ['title', 'slug', 'language', 'template']}),
        (_('Comments settings'),
            {'fields': ['is_commented', 'is_moderated']}),
        (None, 
            {'fields': ['sort_order']}),
    )

    def display_count(self, obj):
        return obj.resources.drafts().count() + obj.persons.drafts().count()
    display_count.short_description = _('Count')

    def display_page(self, obj):
        pages = [ cat.page for cat in obj.catz.public().distinct() ]
        pages = set(pages)
        return render_to_string("admin/history_category_pages.html", {'pages': pages})
    display_page.allow_tags = True
    display_page.short_description = _('Page')

# --------------------------------------------------------------------------- #

