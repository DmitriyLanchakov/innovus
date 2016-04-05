from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User
from annoying.functions import get_object_or_None
from openteam.utils import send_email
from profile.models import Claim
import time

random_password = User.objects.make_random_password


class Command(NoArgsCommand):
    help = "My shiny new management command."

    def handle_noargs(self, **options):
        for claim in Claim.objects.all():
            user = get_object_or_None(User, id=claim.user_id)
            if not user:
                user = get_object_or_None(User, username=claim.email)
                if not user and claim.email and claim.user_id:
                    password = random_password()
                    new_user = User(
                        id = claim.user_id,
                        username = claim.email,
                        first_name = claim.first_name,
                        last_name = claim.last_name,
                        email = claim.email)
                    new_user.set_password(password)
                    new_user.save()
                    claim.user = new_user
                    claim.save()
                    send_email(claim.email, 'new_password', {'login': claim.email, 'password': password})
                    print 'proceed %s' % claim.email
                    time.sleep(1)
                elif user and not claim.delegation_manager_id:
                    print claim.email, user.id

