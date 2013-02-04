from goscale.cms_plugins import GoscaleCMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import models

GOSCALE_PRESENTATIONS_PLUGIN_TEMPLATES = getattr(settings, 'GOSCALE_PRESENTATIONS_PLUGIN_TEMPLATES', (
    ('presentation.html', _('Presentation')),
)) + getattr(settings, 'GOSCALE_PRESENTATIONS_CUSTOM_PLUGIN_TEMPLATES', ())


class GooglePresentationPlugin(GoscaleCMSPluginBase):
    """
    Google Presentation plugin for GoScale
    """
    model = models.GooglePresentation
    name = _("Google Presentation")
    plugin_templates = GOSCALE_PRESENTATIONS_PLUGIN_TEMPLATES
    render_template = GOSCALE_PRESENTATIONS_PLUGIN_TEMPLATES[0][0]
    fieldsets = [
        [_('Presentation options'), {
            'fields': ['embed', 'width', 'height', 'ratio', 'embed_as_is', 'delay', 'autoplay', 'loop']
        }]
    ]

plugin_pool.register_plugin(GooglePresentationPlugin)


class SlidesharePlugin(GoscaleCMSPluginBase):
    """
    Slideshare Presentation plugin for GoScale
    """
    model = models.Slideshare
    name = _("Slideshare Presentation")
    plugin_templates = GOSCALE_PRESENTATIONS_PLUGIN_TEMPLATES
    render_template = GOSCALE_PRESENTATIONS_PLUGIN_TEMPLATES[0][0]
    fieldsets = [
        [_('Presentation options'), {
            'fields': ['embed', 'width', 'height', 'ratio', 'embed_as_is', 'start', 'without_related_content']
        }]
    ]

plugin_pool.register_plugin(SlidesharePlugin)


class SpeakerdeckPlugin(GoscaleCMSPluginBase):
    """
    Speakerdeck Presentation plugin for GoScale
    """
    model = models.Speakerdeck
    name = _("Speakerdeck Presentation")
    plugin_templates = GOSCALE_PRESENTATIONS_PLUGIN_TEMPLATES
    render_template = GOSCALE_PRESENTATIONS_PLUGIN_TEMPLATES[0][0]
    fieldsets = [
        [_('Presentation options'), {
            'fields': ['embed', 'width', 'height', 'ratio', 'embed_as_is', 'start']
        }]
    ]

plugin_pool.register_plugin(SpeakerdeckPlugin)