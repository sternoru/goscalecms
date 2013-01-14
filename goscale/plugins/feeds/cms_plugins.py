from goscale.cms_plugins import GoscaleCMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import models

GOSCALE_FEEDS_PLUGIN_TEMPLATES = getattr(settings, 'GOSCALE_FEEDS_PLUGIN_TEMPLATES', (
    ('posts.html', _('Posts')),
    ('posts_small.html', _('Small posts (sidebar)')),
)) + getattr(settings, 'GOSCALE_FEEDS_CUSTOM_PLUGIN_TEMPLATES', ())


class FeedPlugin(GoscaleCMSPluginBase):
    """
    Feed plugin for GoScale
    """
    model = models.Feed
    name = _("RSS Feed")
    plugin_templates = GOSCALE_FEEDS_PLUGIN_TEMPLATES
    render_template = GOSCALE_FEEDS_PLUGIN_TEMPLATES[0][0]
    fieldsets = [
        [_('Feed options'), {
            'fields': ['url', 'page_size', 'show_date', 'external_links']
        }]
    ]

plugin_pool.register_plugin(FeedPlugin)