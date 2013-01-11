from goscale.cms_plugins import GoscaleCMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
import models

PLUGIN_TEMPLATES = (
    ('events.html', _('Events list')),
    ('events_mini.html', _('Events mini list (sidebar)')),
)

class CalendarPlugin(GoscaleCMSPluginBase):
    """
    Google Calendar plugin for GoScale
    """
    model = models.Calendar
    name = _("Calendar")
    plugin_templates = PLUGIN_TEMPLATES
    render_template = PLUGIN_TEMPLATES[0][0]
    plugin_post_template = 'event.html'
    fieldsets = [
        [_('Calendar options'), {
            'fields': ['url', 'show_datepicker', 'show_past']
        }]
    ]

plugin_pool.register_plugin(CalendarPlugin)