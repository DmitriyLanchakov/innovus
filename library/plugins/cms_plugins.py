from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from library.models.resources import (Resource, Video, Audio, Document,
        Picture, ResourceToCategory)
from library.models.persons import Person, PersonToCategory
from library.plugins.models import (Resources, PersonsOnIndex, PersonsList,
    PersonsInCategory)



class ResourcesCategoryPlugin(CMSPluginBase):
    admin_preview = False
    model = Resources
    name = _('Last resources from given category')
    render_template = 'plugins/resources.html'
    filter_horizontal = ('categories', )

    def render(self, context, instance, placeholder):
        self.render_template = instance.template or self.render_template
        categories = instance.categories.all()
        resources = self.resource_model().objects.filter(
            category__in=instance.categories.all())[:instance.count]
        res_positions = ResourceToCategory.objects.filter(
                category__in=instance.categories.all(),
                related_model__in=self.resource_model().objects.all(),
            ).order_by('sort_order')[:instance.count]
        resources = [position.resource() for position in res_positions]
        context.update({
            'resources': resources,
            'categories': categories,
            'object': instance,
            'placeholder': placeholder,
        })
        return context

    def resource_model(self):
        return Resource


class VideoCategoryPlugin(ResourcesCategoryPlugin):
    render_template = 'plugins/resources/videos.html'
    name = _('Last videos from given category')

    def resource_model(self):
        return Video


class AudioCategoryPlugin(ResourcesCategoryPlugin):
    render_template = 'plugins/resources/audio.html'
    name = _('Last audio from given category')

    def resource_model(self):
        return Audio


class DocumentCategoryPlugin(ResourcesCategoryPlugin):
    render_template = 'plugins/resources/documents.html'
    name = _('Last documents from given category')

    def resource_model(self):
        return Document


class PictureCategoryPlugin(ResourcesCategoryPlugin):
    render_template = 'plugins/resources/pictures.html'
    name = _('Last pictures from given category')

    def resource_model(self):
        return Picture


class PersonsPlugin(CMSPluginBase):
    admin_preview = False
    model = PersonsList
    name = _("Persons list")
    render_template = "plugins/persons.html"
    filter_horizontal = ('categories', )

    def render(self, context, instance, placeholder):
        positions = PersonToCategory.objects.filter(
                category__in=instance.categories.all(),
                related_model__in=Person.objects.all()).order_by('sort_order')
        if instance.sorting == 1:
            positions = positions.order_by('related_model__name')
        self.render_template = instance.template or self.render_template
        context.update({
            'positions': positions[:instance.per_page],
            'object'      : instance,
            'placeholder' : placeholder,
        })
        return context


class PersonListOnPagePlugin(CMSPluginBase):
    admin_preview = False
    model = PersonsInCategory
    name = _("Persons category on page")
    render_template = "plugins/persons.html"

    def render(self, context, instance, placeholder):
        positions = PersonToCategory.objects.filter(
                category=instance.category,
                related_model__in=instance.category.persons.all()).order_by('sort_order')
        if instance.sorting == 1:
            positions = positions.order_by('related_model__name')
        self.render_template = instance.template or self.render_template
        context.update({
            'positions': positions[:instance.per_page],
            'object': instance,
            'placeholder': placeholder,
        })
        return context


class PersonsOnIndexPlugin(CMSPluginBase):
    admin_preview = False
    model = PersonsOnIndex
    name = _("persons on index page")
    render_template = settings.PERSONS_LIST_TEMPLATES[0][0]

    def render(self, context, instance, placeholder):
        speakers = PersonToCategory.objects.filter(
                category=instance.speakers,
                related_model__in=instance.speakers.persons.all()).order_by('sort_order')
        interviews = PersonToCategory.objects.filter(
                category=instance.interviews,
                related_model__in=instance.interviews.persons.all()).order_by('sort_order')
        if instance.sorting == 1:
            speakers = speakers.order_by('related_model__name')
            interviews = interviews.order_by('related_model__name') 
        self.render_template = instance.template or self.render_template
        context.update({
            'speakers': speakers[:instance.speakers_count],
            'interviews': interviews[:instance.interviews_count],
            'objects': instance,
            'placeholder': placeholder,
        })
        return context


plugin_pool.register_plugin(ResourcesCategoryPlugin)
plugin_pool.register_plugin(VideoCategoryPlugin)
plugin_pool.register_plugin(AudioCategoryPlugin)
plugin_pool.register_plugin(DocumentCategoryPlugin)
plugin_pool.register_plugin(PictureCategoryPlugin)
plugin_pool.register_plugin(PersonsOnIndexPlugin)
plugin_pool.register_plugin(PersonsPlugin)
plugin_pool.register_plugin(PersonListOnPagePlugin)

