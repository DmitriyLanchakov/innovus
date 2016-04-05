from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from tinymce.widgets import TinyMCE
from publisher_admin.admin import SortableAdmin


class PersonAdmin(SortableAdmin):
    list_display = (
        'name', 'display_position', 'display_photo',
        'is_commented', 'is_moderated',
    )
    list_filter  = (
        'language', 'category',
        'is_commented', 'is_moderated',
    )
    
    search_fields = ('name',)
    change_list_template = "admin/library/resource/change_list.html"

    filter_horizontal = ('category', )

    fieldsets = (
        (None, {
            'fields': ['name', 'slug', 'language', 'position', 'photo', ],
            'classes': [],
        }),
        (_('Annotation'), {
            'fields': ['announce', ],
            'classes': ['collapse', ],
        }),
        (None, {
            'fields': ['content', ],
            'classes': [],
        }),
        (_('Tagging'),{
            'fields': ['tags', ],
            'classes': [],
        }),
        (_('Categories'), {
             'fields': ['category', ],
             'classes': [],
        }),
        (_('Comments settings'), {
            'fields': ['is_commented', 'is_moderated', ],
        }),
    )

    prepopulated_fields = {'slug': ['name',]}
    formfield_overrides = {models.TextField: {'widget': TinyMCE}}

    def display_position(self, object):
        return object.position

    display_position.allow_tags = True
    display_position.short_description = _('Position')

    def display_photo(self, object):
        return render_to_string('admin/persons/display_photo.html', {'object': object})

    display_photo.allow_tags = True
    display_photo.short_description = _('Photo')

    class Media:
        css = {
            'screen': (
                settings.CSS_URL + 'admin/inline_form.css',
                settings.CSS_URL + 'admin/dev_style.css',
                settings.CSS_URL + 'smoothness/jquery-ui-1.8.11.custom.css',
                settings.CSS_URL + 'admin/history-dropdown.css'
            )
        }
        js = (
            settings.JS_URL + 'admin/history-dropdown.js',
            settings.JS_URL + 'TinyMCEAdmin.js',
        )

