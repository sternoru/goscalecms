from django import forms
from cms.plugin_base import CMSPluginBase
from goscale.models import GoscaleCMSPlugin

class GoscaleCMSPluginBase(CMSPluginBase):
    """
    Base class for GoScale plugins
    """
    exclude = ('posts',)
    plugin_templates = None

    def get_form(self, *args, **kwargs):
        form = super(GoscaleCMSPluginBase, self).get_form(*args, **kwargs)
        if self.plugin_templates:
            form.base_fields['template'] = forms.ChoiceField(choices=self.plugin_templates)
            print form.base_fields['template'].choices
        return form

    def render(self, context, instance, placeholder):
        if instance and instance.template:
            self.render_template = instance.template
        context['posts'] = [post.json() for post in instance.posts.all()]
        return context