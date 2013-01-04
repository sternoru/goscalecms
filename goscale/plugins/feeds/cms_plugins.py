from goscale.cms_plugins import GoscaleCMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
import models

PLUGIN_TEMPLATES = (
    ('posts.html', _('Posts')),
    ('posts_small.html', _('Small posts (sidebar)')),
)

class FeedPlugin(GoscaleCMSPluginBase):
    """
    Feed plugin for GoScale
    """
    model = models.Feed
    name = _("RSS Feed (GoSCale)")
    plugin_templates = PLUGIN_TEMPLATES
    render_template = PLUGIN_TEMPLATES[0][0]

plugin_pool.register_plugin(FeedPlugin)