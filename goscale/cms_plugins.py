import simplejson

from django import forms
from cms.plugin_base import CMSPluginBase
from goscale.models import GoscaleCMSPlugin

class GoscaleCMSPluginBase(CMSPluginBase):
    """
    Base class for GoScale plugins
    """
    exclude = ['posts',]
    plugin_templates = None

    def get_form(self, *args, **kwargs):
        form = super(GoscaleCMSPluginBase, self).get_form(*args, **kwargs)
        if self.plugin_templates:
            form.base_fields['template'] = forms.ChoiceField(choices=self.plugin_templates)
            print form.base_fields['template'].choices
        else:
            self.exclude.append('template')
        return form

    def render(self, context, instance, placeholder):
        if instance and instance.template:
            self.render_template = instance.template
        extra_context = {}
        extra_context['posts'] = instance.get_posts()
        ignore_fields = ['changed_date', 'cmsplugin', 'cmsplugin_ptr', 'creation_date', 'id', 'language', 'level',
                        'lft', 'parent', 'placeholder', 'plugin_type', 'posts', 'rght', 'tree_id']
        for field in instance._meta.get_all_field_names():
            if field not in ignore_fields:
                extra_context[field] = instance.__getattribute__(field)
        extra_context['debug'] = simplejson.dumps(extra_context, indent=4)
        context.update(extra_context)
        return context