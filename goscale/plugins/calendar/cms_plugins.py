from goscale.cms_plugins import GoscaleCMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import models

GOSCALE_CALENDAR_PLUGIN_TEMPLATES = getattr(settings, 'GOSCALE_CALENDAR_PLUGIN_TEMPLATES', (
    ('events.html', _('Events list')),
    ('events_mini.html', _('Events mini list (sidebar)')),
    ('datepicker.html', _('Date picker widget')),
)) + getattr(settings, 'GOSCALE_CALENDAR_CUSTOM_PLUGIN_TEMPLATES', ())


class CalendarPlugin(GoscaleCMSPluginBase):
    """
    Google Calendar plugin for GoScale
    """
    model = models.Calendar
    name = _("Calendar")
    plugin_templates = GOSCALE_CALENDAR_PLUGIN_TEMPLATES
    render_template = GOSCALE_CALENDAR_PLUGIN_TEMPLATES[0][0]
    plugin_post_template = 'event.html'
    fieldsets = [
        [_('Calendar options'), {
            'fields': ['url', 'page_size', 'show_past']
        }]
    ]

    def _extra_context(self, context, instance):
        if instance.show_past:
            return {'past_events': instance.get_past_events()}
        return super(CalendarPlugin, self)._extra_context(context, instance)

plugin_pool.register_plugin(CalendarPlugin)