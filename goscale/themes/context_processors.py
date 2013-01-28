# -*- coding: utf-8 -*-
import simplejson
from django.conf import settings
from django.contrib.sites.models import get_current_site


def static(request):
    # set  config
    site_theme = settings.THEME
    static_theme_url = '%sthemes/%s/static/' % (settings.STATIC_URL, site_theme)
    static_common_url = '%sthemes/common/static/' % settings.STATIC_URL
    # build the context
    return {
        'site': get_current_site(request),
        'GOSCALE_THEME': site_theme,
        'STATIC_THEME_URL': static_theme_url,
        'STATIC_COMMON_URL': static_common_url,
    }
