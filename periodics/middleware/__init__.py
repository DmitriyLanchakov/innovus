# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

# --------------------------------------------------------------------------- #

class SiteResolver(object):
    def process_view(self, request, view, *view_args, **view_kwargs):
        try:
            request.current_site = Site.objects.get(pk=settings.SITE_ID)

        except Site.DoesNotExist:
            pass

        return None

# --------------------------------------------------------------------------- #   