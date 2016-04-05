# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.conf.urls.defaults import url, patterns
from django.contrib import admin
from django.http import HttpResponse, Http404, HttpResponseForbidden

from django.utils.translation import ugettext as _
from django.template import Template, Context, add_to_builtins, RequestContext
from django.shortcuts import get_object_or_404, redirect, render_to_response

from annoying.functions import get_object_or_None
from annoying.decorators import ajax_request

from tinymce.widgets import TinyMCE
from periodics.models import Category, Comment, Post, BannedIp, Attachment
from periodics.forms import PostAdminForm, CategoryAdminForm
from publisher_admin.admin import PublisherAdmin, SortableAdmin


class CategoryAdmin(SortableAdmin):
    fieldsets = (
        (None, {
            'fields': ['title', ],
        }),
        (_('Preferences'), {
            'classes': ['collapse-closed', ],
            'fields': ['is_commented', 'is_moderated', 'per_page',
                'post_template'],
        })
    )
    list_filter = ('is_commented', 'is_moderated')
    list_display = ('title', 'is_commented', 'is_moderated', 'per_page',
            'created_by', 'modified_by')
    ordering = ('sort_order', 'id')
    search_fields = ('title', )

    def get_urls(self):
        """Adds a custom views to admin site
        """
        return patterns('',
            url('^save/$', self.admin_site.admin_view(self.addform),
                name='periodics_category_addform'),
        ) + super(CategoryAdmin, self).get_urls()

    @ajax_request
    def addform(self, request):
        success, category = None, None

        form = CategoryAdminForm(request.POST or None)
        success = form.is_valid()
        if success:
            category = form.save()
        if request.is_ajax():
            errors = dict()
            for k in form.errors:
                errors[k] = unicode(form._errors[k])
            return {'category': category, 'success': success, 'errors': errors}
        else:
            form = CategoryAdminForm()
        return render_to_response('admin/periodics/category/addform.html', {
            'form': form,
            'success': success,
            'category': category,
            }, context_instance=RequestContext(request))

    class Media:
        css = {
            'screen': (
                '%sjquery.ui.css' % settings.CSS_URL,
                '%scategory_change_list.css' % settings.CSS_URL,
                )
            }


class PostAdmin(PublisherAdmin):
    """
    Post Admin class
    """
    class AttachmentsInline(admin.StackedInline):
        extra = 3
        model = Attachment

    inlines = [AttachmentsInline, ]

    # Use custom form
    form = PostAdminForm
    list_display = ('title', 'modified_by', 'public_from', 'state',
            'publisher_state', 'is_active')
    list_filter = ('is_active', 'category', 'public_from')
    search_fields = ('title', )
    formfield_overrides = {models.TextField: {'widget': TinyMCE}}

    fieldsets = (
        (None, {
            'fields':  ['title', 'tags'],
            'classes': ['main', ],
        }),
        (_('Annotation'), {
            'fields':  ['annotation', ],
            'classes': ['main', 'collapse', 'annotation'],
        }),
        (None, {
            'fields':  ['content', ],
            'classes': ['main', ],
        }),
        (_('Category'), {
            'fields':  ['category', ],
            'classes': ['right-panel', ],
        }),
        (_('Display on site'), {
            'fields':  ['is_active', 'public_from', 'public_till'],
            'classes': ['display', 'collapse', ],
        }),
        (_('Picture'), {
            'fields':  ['picture_src', 'picture_show', 'picture_alt',
                'picture_title'],
            'classes': ['main', 'collapse', 'picture'],
        }),
        (_('Gallery'), {
            'fields': ['gallery', ],
            'classes': ['comments', 'collapse'],
        }),
        (_('Comments'), {
            'fields':  ['comments_allow', 'comments_premoderate'],
            'classes': ['comments', 'collapse'],
        }),
    )

    def get_urls(self):
        """Adds a custom views to admin site
        """
        return patterns('',
            url('^publish/$', self.admin_site.admin_view(self.publish),
                name='publish'),
        ) + super(PostAdmin, self).get_urls()

    def publish(self, request):
        try:
            object_id = int(request.POST.get('object_id'))
        except KeyError:
            return HttpResponseForbidden()
        try:
            instance = Post.admin_objects.get(pk=object_id)
            instance.publish()
        except Post.DoesNotExist:
            raise Http404
        return HttpResponse(status=200)

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user.username
        obj.save()

    def state(self, obj):
        """Displays post state
        """
        if obj.publisher_public:
            return _('Published')
        else:
            return _('Draft')

    state.admin_order_field = 'publisher_public'

    def comments_count(self, obj):
        """Displays number of comments for each post in admin area
        """
        if obj.publisher_public:
            return obj.publisher_public.comments.count() or 0
        else:
            return obj.comments.count() or 0

    def queryset(self, request):
        """Queryset to show items in list
        """
        return self.model.objects.drafts()

    class Media:
        js = [
            settings.JS_URL + 'lib/jquery-ui-1.8.11.custom.min.js',
            settings.JS_URL + 'admin/post-admin.js',
            settings.JS_URL + 'admin/category-admin.js',
            settings.JS_URL + 'admin/comments-admin.js',
            settings.JS_URL + 'TinyMCEAdmin.js',
        ]
        css = {
            'screen': (
                settings.CSS_URL + 'admin/main.css',
                settings.CSS_URL + 'admin/page_form.css',
                settings.CSS_URL + 'admin/jquery.ui.css',
                settings.CSS_URL + 'admin/ui-theme.css',
            )
        }


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'clean_content', 'display_author', 'link',
            'ip_address', 'created_at', 'is_approved', 'toggle', 'ban')
    list_filter = ('is_approved', )
    actions = ('action_approve', 'action_blame')
    raw_id_fields = ('parent', )
    date_hierarchy = 'created_at'
    list_per_page = 40

    def display_author(self, obj):
        return obj.user if obj.user is not None else obj.author_name
    display_author.short_description = _('Author')

    def action_approve(self, request, queryset):
        row = queryset.update(is_approved=True)
        msg = "1 comment was" if row == 1 else "%s comments were" % row
        self.message_user(request, "%s successfully approved." % msg)
    action_approve.short_description = _('Approve selected comments')

    def action_hide(self, request, queryset):
        row = queryset.update(is_approved=False)
        msg = "1 comment was" if row == 1 else "%s comments were" % row
        self.message_user(request, "%s successfully disapproved." % msg)
    action_hide.short_description = _('Hide selected comments')

    def approve(self, obj):
        return '[<a href="?">approve</a>]'
    approve.allow_tags = True
    approve.short_description = _('Approve')

    def hide(self, obj):
        return '[<a href="?">disapprove</a>]'
    hide.allow_tags = True
    hide.short_description = _('Hide')

    @ajax_request
    def comment_approve(self, request, comment_id, approved=False,
            toggle=False):
        """Custom view toggles comment approvement
        """
        comment = get_object_or_404(Comment, pk=comment_id)
        if toggle:
            approved = not comment.is_approved
        comment.is_approved = approved
        comment.save()
        if request.is_ajax():
            return {
                'approved': approved,
                'toggle': toggle,
                'new_label': unicode(_('Blame') if approved else _('Approve'))
            }
        else:
            if approved:
                message = _('Comment successfully approved')
            else:
                message = _('Comment successfully blamed')

            request.user.message_set.create(message=message)
            return redirect(request.META.get('HTTP_REFERER'))

    def get_urls(self):
        """
        Adds a custom views to admin site
        """
        return patterns('',
            url('^(?P<comment_id>\d+)/approve/$',
                self.admin_site.admin_view(self.comment_approve),
                {'approved': True}, name='periodics_comment_approve'),
            url('^(?P<comment_id>\d+)/disapprove/$',
                self.admin_site.admin_view(self.comment_approve),
                {'approved': False}, name='periodics_comment_disapprove'),
            url('^(?P<comment_id>\d+)/toggle/$',
                self.admin_site.admin_view(self.comment_approve),
                {'toggle': True}, name='periodics_comment_toggle'),
        ) + super(CommentAdmin, self).get_urls()

    # ---------------------------------------------------------------------- #

    def action_helper(self, request, queryset, flag, suffix):
        row = queryset.update(is_approved=flag)
        msg = "1 comment was" if row == 1 else "%s comments were" % row
        self.message_user(request, "%s successfully %s." % (msg, suffix))

    def action_blame(self, request, queryset):
        self.action_helper(request, queryset, False, 'blamed')

    action_approve.short_description = _('Approve selected comments')
    action_blame.short_description    = _('Blame selected comments')

    # ---------------------------------------------------------------------- #

    def toggle(self, obj):
        """
        Generates HTML to toggle comment approvement column
        """
        label = _('Blame') if obj.is_approved else _('Approve')
        add_to_builtins('django.templatetags.i18n')

        tpl  = '<a class="approve-comment-button" href="'
        tpl += '{% url admin:periodics_comment_toggle comment.id %}">'
        tpl += '{{ label }}</a>'

        return Template(tpl).render(Context({'comment': obj, 'label':label}))

    def ban(self, obj):
        """
        Generates HTML for 'Ban author' column
        """
        label = _('Ban IP')
        add_to_builtins('django.templatetags.i18n')

        tpl  = '<a class="ban-ip-button" href="'
        tpl += '{% url admin:periodics_ban_toggle comment.ip_address %}">'
        tpl += '{{ label }}</a>'

        return Template(tpl).render(Context({'comment': obj, 'label':label}))

    def link(self, comment):
        """
        Generates link to post
        """
        obj  = comment.commentable
        attr = 'public' if obj.publisher_is_draft else 'draft'
        post = getattr(obj, 'publisher_%s' % attr )

        return '<a href="../../%(application)s/%(module_name)s/%(post_id)s/">%(title)s</a>' % {
            'application' : post._meta.app_label,
            'module_name' : post._meta.module_name,
            'post_id'     : post.pk,
            'title'       : unicode(post),
        }

    toggle.allow_tags = True
    toggle.short_description = _('Toggle approvement')

    ban.allow_tags = True
    ban.short_description = _('Ban author')

    link.allow_tags = True
    link.short_description = _('Link to post')

    # ---------------------------------------------------------------------- #

    class Media:
        js = (
            settings.JS_URL + 'lib/jquery.min.js',
            settings.JS_URL + 'lib/jquery-ui-1.8.11.custom.min.js',
            settings.JS_URL + 'js/admin/comments-admin.js',
        )

# --------------------------------------------------------------------------- #

class BannedIpAdmin(admin.ModelAdmin):
    def get_urls(self):
        """
        Adds a custom views to admin site
        """
        return patterns('',
            url('^(?P<ip>.+)/add/$', self.admin_site.admin_view(self.ban),
                name='periodics_ban_add'),
            url('^(?P<ip>.+)/toggle/$', self.admin_site.admin_view(self.ban),
                {'toggle': True}, name='periodics_ban_toggle'),
            ) + super(BannedIpAdmin, self).get_urls()

    @ajax_request
    def ban(self, request, ip, toggle=True):
        """
        Creates or removes bans
        """
        ban, created = get_object_or_None(BannedIp, ip_address=ip), False

        if ban:
            if toggle:
                delete = ban.delete()

        else:
            ban = BannedIp.objects.create(
                ip_address = ip,
                banned_by  = request.user,
                reason     = request.POST.get('reason', ''),
            )
            created = True

        if request.is_ajax():
            return {'created': created}

        else:
            if created:
                message = _('Ip address %s successfully banned' % ip)
            else:
                message = _('Ip address %s is already banned, not created' % ip)

            request.user.message_set.create(message=message)
            return redirect(request.META.get('HTTP_REFERER', '..'))

    list_display = ('ip_address', 'banned_at', 'banned_by', 'reason', )
    raw_id_fields = ('banned_by', )


class AttachmentAdmin(admin.ModelAdmin):

    def file_size(self, obj):
        return obj.file.size

    list_display = ('title', 'file', 'file_size',)
    raw_id_fields = ('post', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(BannedIp, BannedIpAdmin)
admin.site.register(Attachment, AttachmentAdmin)

