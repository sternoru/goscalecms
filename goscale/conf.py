import os

from django.conf import settings

gettext_noop = lambda s: s

DEFAULT_LANGUAGE = getattr(settings, 'DEFAULT_LANGUAGE', 'en')

""" Goscale Plugin settings """

GOSCALE_DEFAULT_POST_PLUGIN = getattr(settings, 'GOSCALE_DEFAULT_POST_PLUGIN', 'post.html')

# Settings defined inside of the plugins
# goscale.plugins.videos.cms_plugins.GOSCALE_VIDEOS_PLUGIN_TEMPLATES
# goscale.plugins.videos.cms_plugins.GOSCALE_VIDEOS_CUSTOM_PLUGIN_TEMPLATES
# goscale.plugins.calendar.cms_plugins.GOSCALE_CALENDAR_PLUGIN_TEMPLATES
# goscale.plugins.calendar.cms_plugins.GOSCALE_CALENDAR_CUSTOM_PLUGIN_TEMPLATES
# goscale.plugins.feeds.cms_plugins.GOSCALE_FEEDS_PLUGIN_TEMPLATES
# goscale.plugins.feeds.cms_plugins.GOSCALE_FEEDS_CUSTOM_PLUGIN_TEMPLATES
# goscale.plugins.forms.cms_plugins.GOSCALE_FORMS_PLUGIN_TEMPLATES
# goscale.plugins.forms.cms_plugins.GOSCALE_FORMS_CUSTOM_PLUGIN_TEMPLATES
# goscale.plugins.pictures.cms_plugins.GOSCALE_PICTURES_PLUGIN_TEMPLATES
# goscale.plugins.pictures.cms_plugins.GOSCALE_PICTURES_CUSTOM_PLUGIN_TEMPLATES



""" Goscale technical settings """

# how often posts should be updated from the source
GOSCALE_POSTS_UPDATE_FREQUENCY = getattr(settings, 'GOSCALE_POSTS_UPDATE_FREQUENCY', 60*30) # 30 minutes

#set this if you want to use django's cache in production
GOSCALE_CACHE_DURATION = getattr(
    settings,
    'GOSCALE_CACHE_DURATION',
    getattr(settings, 'CMS_CACHE_DURATIONS', {'content': 1})['content']
)
#set this if you want to use browser cache for your site on production
GOSCALE_BROWSER_CACHE_MAX_AGE = getattr(settings, 'GOSCALE_CACHE_DURATION', GOSCALE_CACHE_DURATION)

# UTC by default, better set it to some timezone delta
#of a timezone your cusomters are most likely in
GOSCALE_STANDARD_TZ_DELTA = getattr(settings, 'GOSCALE_STANDARD_TZ_DELTA', 0)

#when stripping short content from an app, specify how long this
#short content (number of characters) it will be
GOSCALE_POST_SUMMARY_LIMIT = getattr(settings, 'GOSCALE_POST_SUMMARY_LIMIT', 300)

GOSCALE_DEFAULT_PAGE_SIZE = getattr(settings, 'GOSCALE_DEFAULT_PAGE_SIZE', 10)

#if you plan to use a module which is using GoScale's "blogger" content
#type (see GOSCALE_CONTENT_TYPES and GOSCALE_MODULES setting)
#please set this to a fallback blogname (from blogspot,com)
GOSCALE_DEFAULT_BLOG = getattr(settings, 'DEFAULT_BLOG', '')

#set this if you want to use a GoScale module with source which need these to be provided
#for example calendar source need it to retrieve calendar via the Google data API
#from this Google Accounts calendar
GOSCALE_GOOGLE_ACCOUNT = getattr(settings, 'GOSCALE_GOOGLE_ACCOUNT', '')
GOSCALE_GOOGLE_ACCOUNT_PASSWORD = getattr(settings, 'GOSCALE_GOOGLE_ACCOUNT_PASSWORD', '')

# indent to show for JSON output in DEBUG and non DEBUG mode? 
GOSCALE_JSON_INDENT = getattr(settings, 'GOSCALE_JSON_INDENT', 4 if settings.DEBUG else 0)

# the default order of the content, since GoScale's main content model
# os goscale.models.Post it defaults to '-published' (show newst posts first)
# if you decide to use a different model you can overwrite this setting
GOSCALE_DEFAULT_CONTENT_ORDER = getattr(settings, 'GOSCALE_DEFAULT_CONTENT_ORDER', '-published')

# ------------------------------------------ 
"""
GoScale Don't Change settings
"""

GOSCALE_ROOT_TEMPLATE_DIR = 'goscale'

# atom datetime format
GOSCALE_ATOM_DATETIME_FORMAT = getattr(settings, 'GOSCALE_ATOM_DATETIME_FORMAT', '%Y-%m-%dT%H:%M:%S') #without timezone
# rss datetime format
GOSCALE_RSS_DATETIME_FORMAT = getattr(settings, 'GOSCALE_RSS_DATETIME_FORMAT', '%a, %d %b %Y %H:%M:%S')  #without timezone

# Supported output formats for goscale modules and their content
# only change when you extend GoScale
GOSCALE_SUPPORTED_OUTPUT_FORMATS = getattr(settings, 'GOSCALE_SUPPORTED_OUTPUT_FORMATS', ['html','rss','json', 'atom'])