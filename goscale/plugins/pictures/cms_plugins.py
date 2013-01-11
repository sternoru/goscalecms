from goscale.cms_plugins import GoscaleCMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
import models

PLUGIN_TEMPLATES = (
    ('grid.html', _('Grid')),
    ('slideshow.html', _('Slideshow')),
    ('slideshow_with_thumbnails.html', _('Slideshow with thumbnails')),
    ('slideshow_mini.html', _('Mini slideshow (sidebar)')),
)

class PicasaPlugin(GoscaleCMSPluginBase):
    """
    Feed plugin for GoScale
    """
    model = models.Picasa
    name = _("Picasa")
    plugin_templates = PLUGIN_TEMPLATES
    render_template = PLUGIN_TEMPLATES[0][0]
    fieldsets = [
        [_('Pictures options'), {
            'fields': ['url', 'width', 'height', 'thumbnail_width', 'thumbnail_height', 'autoplay']
        }]
    ]

plugin_pool.register_plugin(PicasaPlugin)