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

# Supported content types in GoScale
# only change when you extend GoScale
GOSCALE_CONTENT_TYPES = {
    'rssFeed': {                # data source type name
        'type': 'text',        #content type
        'attributes': {             # language independent settings:
            'url': ('RSS/Atom feed URL', 'url'),
        },
    },
    'blogger': {
        'type': 'text',
        'attributes': { 
            'label': ('Blog labels/tags', 'string'),
            'blog': ('Blog', 'string'),
        }
    },
    'youtube': {
        'type': 'video',
        'attributes': { 
            'channel': ('YouTube channel', 'string'),
            'playlist': ('YouTube playlist', 'string'),
        }
    },
    'vimeo': {
        'type': 'video',
        'attributes': { 
            'channel': ('Vimeo channel', 'string'),
            'album': ('Vimeo album', 'string'),
            'user': ('Vimeo user', 'string'),
        }
    },
    'youku': {
        'type': 'video',
        'attributes': { 
            'playlist': ('Youku playlist', 'string'),
        }
    },
    'picasa': {
        'type': 'photo',
        'attributes': { 
            'user': ('Picasa user', 'string'),
            'albums': ('Picasa albums list', 'list'),
        }
    },
    'calendar': {
        'type': 'calendar',
        'attributes': { 
            'calendar': ('Calendar id', 'string'),
        }
    },
    'static': {
        'type': 'static',
        'attributes': { 
            'title': ('Title', 'string'),
            'text': ('Text', 'text'),            
        }
    },
    'latest': {
        'type': 'text',
        'attributes': { 
            'data_source_list': ('List of data source id\'s', 'sourcelist'), #in save pages/get_pages an array of ids
        }
    },
    # New content type template
    #'newtype': { # data source type name
    #    'name': '', # title for the admin page
    #    'type': '', # content type (ex: text, photo, video, etc...)
    #    'attributes': { # attributes (language dependent)
    #        '': ('', 'string'),
    #    },
    #},    
}

# Supported template layouts in GoScale
# only change when you extend GoScale
GOSCALE_TEMPLATES = {
    'two_columns': {
        'name':'Two columns layout (sidebar on the right)',
        'template':'two_columns.html',        
        'panels': ['sidebar'],        
    },
    # New template/layout
    #'newtemplate': { # name to be stored in Page.template
    #    'name':'', # name for an admin interface
    #    'template':'.html', # template file        
    #    'panels': [], # additional panels to be implemented in this template        
    #},
}

# Supported modules in GoScale
# only change when you extend GoScale
GOSCALE_MODULES = {
    # Main content modules (with paginator and stuff)
    'text_posts': {
        'template': 'text_posts.html',
        'container_template': 'pager_container.html',        
        'js': (),
        'css': (), 
        'name': 'Feed of text posts (blog/news)',
        'content':'text',
        'attributes': {},
    },
    'videos': {
        'template': 'videos.html',
        'container_template': 'videos_container.html',                
        'js': ('videos.js',),
        'css': (), 
        'name': 'Videos (Youtube/Vimeo/Youku/etc)',
        'content':'video',
        'attributes': {},
    },
    # Sidebar modules (small snippets of information
    'latest_posts': {
        'template': 'latest_posts.html',        
        'js': ('latest_posts.js',),
        'css': ('latest_posts.css',), 
        'name': 'Latest blog posts',
        'content':'text',
        'attributes': {},
    },
    'static': {
        'template': 'static.html',        
        'js': (),
        'css': (), 
        'name': 'Static content',
        'content':'static',
        'attributes': {},
    },
    'latest_content': {
        'template': 'latest_content.html',        
        'js': (),
        'css': (), 
        'name': 'Latest mixed content',
        'content':'text',
        'attributes': {},
    },
    # New module template
    #'newmodule': { # module name
    #    'template': '.html', # module content template
    #    'container_template': '.html', # module container template (optional)
    #    'js': (), # module js files
    #    'css': (), # module css files
    #    'name': '', # module title for the admin interface
    #    'content':'text', # module content type (ex: text, photo, video, etc...)
    #    'attributes': {}, # module specific attributes
    #},
}