from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from cms.plugins.text.cms_plugins import TextPlugin
from cms.utils.moderator import get_page_queryset
from django.utils.translation import ugettext_lazy as _
from plugins.models import Toggle, Menu, Sitemap


class TogglePlugin(TextPlugin):
    admin_preview = False
    name = _('Toggle plugin')
    render_template = 'plugins/toggle.html'
    model = Toggle


class SitemapPlugin(CMSPluginBase):
    admin_preview = False
    model = Sitemap
    name = _("Sitemap")
    render_template = "plugins/sitemap.html"


    def render(self, context, instance, placeholder):
        self.render_template = instance.template or SitemapPlugin.render_template
        page_queryset = get_page_queryset(None)
        all_pages = page_queryset.published()
        #.order_by('tree_id', 'parent', 'lft')
        context.update({'pages': all_pages})
        return context


class MenuPlugin(CMSPluginBase):
    admin_preview = False
    model = Menu
    name  = _('Menu plugin')
    render_template = 'plugins/menu.html'

    def render(self, context, instance, placeholder):
        context.update(dict(
            template    = instance.template,
            from_level  = instance.from_level,
            to_level    = instance.to_level,
            extra_active = instance.extra_active,
            extra_inactive = instance.extra_inactive,
            root_id = instance.root_id or '',
            object = instance,
            placeholder = placeholder,
        ))
        return context

plugin_pool.register_plugin(SitemapPlugin)
plugin_pool.register_plugin(MenuPlugin)
plugin_pool.register_plugin(TogglePlugin)

