from annoying.functions import get_object_or_None
from django.core.management.base import BaseCommand
from events.models import ForumEvent, ForumEventContent

class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        src = get_object_or_None(ForumEvent, id=int(args[0]))
        dst = get_object_or_None(ForumEvent, id=int(args[1]))
        dst.event_contents.add(
            ForumEventContent(name=src.name, language=src.language, place=src.place, moderators=src.moderators, cms_page=src.cms_page),
            ForumEventContent(name=dst.name, language=dst.language, place=dst.place, moderators=dst.moderators, cms_page=dst.cms_page),
        )
        for claim in src.registered.all():
            dst.registered.add(claim)
        src.delete()
