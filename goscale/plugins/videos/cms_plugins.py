from goscale.cms_plugins import GoscaleCMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
import models

PLUGIN_TEMPLATES = (
    ('videos.html', _('Videos inline')),
)

class YouKuPlugin(GoscaleCMSPluginBase):
    """
    Videos plugin for GoScale
    """
    model = models.YouKu
    name = _("YouKu")
    plugin_templates = PLUGIN_TEMPLATES
    render_template = PLUGIN_TEMPLATES[0][0]

    fieldsets = [
        [_('Video options'), {'fields': ['playlist', 'lightbox',]}]
    ]

plugin_pool.register_plugin(YouKuPlugin)