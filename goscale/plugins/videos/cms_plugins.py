from goscale.plugins.cms_plugins import GoscaleCMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
import models

class YouKuPlugin(GoscaleCMSPluginBase):
    """
    Videos plugin for GoScale
    """
    model = models.YouKu
    name = _("YouKu Videos (GoSCale)")
    render_template = "videos.html"

plugin_pool.register_plugin(YouKuPlugin)