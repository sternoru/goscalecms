from goscale.cms_plugins import GoscaleCMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import models

GOSCALE_PICTURES_PLUGIN_TEMPLATES = getattr(settings, 'GOSCALE_PICTURES_PLUGIN_TEMPLATES', (
    ('grid.html', _('Grid')),
    ('slideshow.html', _('Slideshow')),
    ('slideshow_with_thumbnails.html', _('Slideshow with thumbnails')),
    ('slideshow_mini.html', _('Mini slideshow (sidebar)')),
    ('carousel_mini.html', _('Mini carousel (sidebar)')),
)) + getattr(settings, 'GOSCALE_PICTURES_CUSTOM_PLUGIN_TEMPLATES', ())


class PicasaPlugin(GoscaleCMSPluginBase):
    """
    Feed plugin for GoScale
    """
    model = models.Picasa
    name = _("Picasa")
    plugin_templates = GOSCALE_PICTURES_PLUGIN_TEMPLATES
    render_template = GOSCALE_PICTURES_PLUGIN_TEMPLATES[0][0]
    fieldsets = [
        [_('Pictures options'), {
            'fields': ['url', 'width', 'height', 'thumbnail_width', 'thumbnail_height', 'autoplay']
        }]
    ]

plugin_pool.register_plugin(PicasaPlugin)