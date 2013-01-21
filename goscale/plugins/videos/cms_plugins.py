from goscale.cms_plugins import GoscaleCMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import models

GOSCALE_VIDEOS_PLUGIN_TEMPLATES = getattr(settings, 'GOSCALE_VIDEOS_PLUGIN_TEMPLATES', (
    ('videos.html', _('Videos')),
)) + getattr(settings, 'GOSCALE_VIDEOS_CUSTOM_PLUGIN_TEMPLATES', ())

class YouKuPlugin(GoscaleCMSPluginBase):
    """
    Videos plugin for GoScale
    """
    model = models.YouKu
    name = _("YouKu")
    plugin_templates = GOSCALE_VIDEOS_PLUGIN_TEMPLATES
    render_template = GOSCALE_VIDEOS_PLUGIN_TEMPLATES[0][0]

    fieldsets = [
        [_('Video options'), {'fields': ['playlist', 'lightbox',]}]
    ]

plugin_pool.register_plugin(YouKuPlugin)