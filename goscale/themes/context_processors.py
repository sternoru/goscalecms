# -*- coding: utf-8 -*-
import simplejson
from django.conf import settings
from django.contrib.sites.models import get_current_site
from goscale import conf


def theme(request):
    # set  config
    site_theme = settings.THEME
    static_theme_url = '%sthemes/%s/static/' % (settings.STATIC_URL, site_theme)
    static_common_url = '%sthemes/common/static/' % settings.STATIC_URL
    config = {}
    settings_list = ['GOSCALE_BOOTSTRAP_THEMES', 'GOSCALE_BOOTSTRAP_THEME',
                     'GOSCALE_AJAXLINKS', 'GOSCALE_AJAXLINKS_EXCEPTIONS']
    for setting in settings_list:
        config[setting] = conf.__dict__.get(setting)
    theme = request.GET.get('theme')
    # build the context
    return {
        'site': get_current_site(request),
        'GOSCALE_THEME': site_theme,
        'STATIC_THEME_URL': static_theme_url,
        'STATIC_COMMON_URL': static_common_url,
        'goscale_config': config,
        'goscale_bootstrap_theme': theme if theme else conf.GOSCALE_BOOTSTRAP_THEME,
        'goscale_config_json': simplejson.dumps(config),
    }
