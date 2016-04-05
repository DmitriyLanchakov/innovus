# encoding: utf-8
from cms.utils import get_language_from_request
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.html import strip_tags, strip_entities, fix_ampersands
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from haystack.query import SearchQuerySet
from annoying.functions import get_object_or_None


class PersonRss(Feed):
    feed_type = Rss201rev2Feed

    def title(self):
        return _('Tomsk forum of innovations')

    def description(self, obj):
        return _('Persons')

    def link(self, obj):
        return "/participants/persons/"

    def get_object(self, request):
        self.url_path = 'http://' + request.META['HTTP_HOST']
        return SearchQuerySet().filter(
                django_ct='library.person',
                language=get_language_from_request(request)
            ).order_by('-django_id')[:10]

    def items(self, obj):
        return obj

    def item_title(self, item):
        return strip_tags(strip_entities("%s - %s" % (item.name, item.position)))

    def item_description(self, item):
        return mark_safe(fix_ampersands(item.announce))

    def item_pubdate(self, item):
        from library.models import Person
        ct = ContentType.objects.get_for_model(Person)
        addition = get_object_or_None(LogEntry, content_type=ct, object_id=item.django_id, action_flag=1)
        return addition.action_time if addition else datetime.now()

    def item_link(self, item):
        return self.url_path + item.url

