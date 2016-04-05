from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django import forms
from events.models import Forum, ForumEvent, ForumEventContent

class ForumAdmin(admin.ModelAdmin):
    exclude = ['created_at', 'updated_at']
    list_display = ['name', 'starts_on', 'ends_on', 'is_current']
    list_editable = ['is_current']
    date_hierarchy = 'starts_on'

    class Meta:
        verbose_name = _('forum')
        verbose_name_plural = _('forums')

admin.site.register(Forum, ForumAdmin)

class ForumEventContentAdmin(admin.StackedInline):
    model = ForumEventContent
    max_num = 2


class ForumEventAdmin(admin.ModelAdmin):
    exclude = ['created_at', 'updated_at']
    list_display = ['display_name', 'can_register_youth', 'can_register_business', 'starts_on', 'ends_on' ]
    list_editable = ['can_register_youth', 'can_register_business', 'starts_on', 'ends_on' ]
    list_filter = ['forum', 'programm_type',]
    ordering = ['starts_on']
    save_on_top = True
#    filter_horizontal = ['speakers', 'moderators']

    formfield_overrides = {models.TextField: { 'widget' : forms.TextInput }, }

    inlines  = [ForumEventContentAdmin,]

    class Media:
        js = [
            settings.JS_URL + 'TinyMCEAdmin.js',
            settings.JS_URL + 'lib/jquery-ui-1.8.11.custom.min.js',
            settings.JS_URL + 'admin/history-dropdown.js',
        ]
        css = {
            'screen': (
                settings.CSS_URL + 'admin/inline_form.css',
                settings.CSS_URL + 'smoothness/jquery-ui-1.8.11.custom.css',
                settings.CSS_URL + 'admin/history-dropdown.css'
            )
        }

    def display_name(self, obj):
        if obj.event_contents.count():
            return "<p>%s</p>" % '</p><p>'.join([content['name'] for content in obj.event_contents.values('name')])
        else:
            return _('no name')
    display_name.short_description = _('name')
    display_name.allow_tags = True


admin.site.register(ForumEvent, ForumEventAdmin)


    
