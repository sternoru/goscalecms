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
        extra_context = {}
        # use template from the instance if provided
        if instance and instance.template:
            self.render_template = instance.template
        # get plugin posts
        extra_context['posts'] = instance.get_posts()
        # get single post if requested
        slug = context['request'].GET.get('post') if 'request' in context else None
        if slug:
            extra_context['post'] = instance.get_post(slug)
        # get plugin attributes
        ignore_fields = ['changed_date', 'cmsplugin', 'cmsplugin_ptr', 'creation_date', 'id', 'language', 'level',
                        'lft', 'parent', 'placeholder', 'plugin_type', 'posts', 'rght', 'tree_id']
        for field in instance._meta.get_all_field_names():
            if field not in ignore_fields:
                extra_context[field] = instance.__getattribute__(field)
        # add debug for development
        extra_context['debug'] = simplejson.dumps(extra_context, indent=4)
        # return updated context
        context.update(extra_context)
        return context