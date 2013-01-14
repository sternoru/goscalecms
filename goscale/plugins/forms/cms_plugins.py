from goscale.cms_plugins import GoscaleCMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
import models

PLUGIN_TEMPLATES = (
    ('form.html', _('Form')),
    ('form_popup.html', _('Form in a lightbox')),
)

class FormPlugin(GoscaleCMSPluginBase):
    """
    Feed plugin for GoScale
    """
    model = models.Form
    name = _("Google Form")
    plugin_templates = PLUGIN_TEMPLATES
    render_template = PLUGIN_TEMPLATES[0][0]
    fieldsets = [
        [_('Form options'), {
            'fields': ['url']
        }]
    ]

plugin_pool.register_plugin(FormPlugin)