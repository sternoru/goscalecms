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
    YouKu videos plugin for GoScale
    """
    model = models.YouKu
    name = _("YouKu")
    plugin_templates = GOSCALE_VIDEOS_PLUGIN_TEMPLATES
    render_template = GOSCALE_VIDEOS_PLUGIN_TEMPLATES[0][0]

    fieldsets = [
        [_('Video options'), {'fields': ['playlist', 'lightbox',]}]
    ]

plugin_pool.register_plugin(YouKuPlugin)

class YoutubePlugin(GoscaleCMSPluginBase):
    """
    YouTube videos plugin for GoScale
    """
    model = models.Youtube
    name = _("YouTube")
    plugin_templates = GOSCALE_VIDEOS_PLUGIN_TEMPLATES
    render_template = GOSCALE_VIDEOS_PLUGIN_TEMPLATES[0][0]

    fieldsets = [
        [_('Video options'), {'fields': ['playlist', 'channel', 'lightbox',]}]
    ]

plugin_pool.register_plugin(YoutubePlugin)

class VimeoPlugin(GoscaleCMSPluginBase):
    """
    Vimeo videos plugin for GoScale
    """
    model = models.Vimeo
    name = _("Vimeo")
    plugin_templates = GOSCALE_VIDEOS_PLUGIN_TEMPLATES
    render_template = GOSCALE_VIDEOS_PLUGIN_TEMPLATES[0][0]

    fieldsets = [
        [_('Video options'), {'fields': ['playlist', 'user', 'lightbox',]}]
    ]

plugin_pool.register_plugin(VimeoPlugin)