import simplejson

from django import forms
from cms.plugin_base import CMSPluginBase
from goscale.models import Post
from goscale import conf
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.loader import render_to_string

class GoscaleCMSPluginBase(CMSPluginBase):
    """
    Base class for GoScale plugins
    """
    module = 'GoScale CMS'
    exclude = ['posts', 'updated']
    parent_fieldset = [_('Default options'), {'fields': ['template', 'title',]}]
    change_form_template = 'admin/plugin_change_form.html'
    plugin_post_template = conf.GOSCALE_DEFAULT_POST_PLUGIN
    plugin_templates = None

    def __init__(self, *args, **kwargs):
        if self.fieldsets:
            if _('Default options') not in self.fieldsets[0]:
                self.fieldsets.insert(0, self.parent_fieldset)
        else:
            fields = self.model.get_fields_list()
            fields.remove('title')
            fields.remove('template')
            self.fieldsets = [
                self.parent_fieldset,
                [_('Plugin options'), {'fields': fields}]
            ]
        super(GoscaleCMSPluginBase, self).__init__(*args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(GoscaleCMSPluginBase, self).get_form(*args, **kwargs)
        if self.plugin_templates and len(self.plugin_templates) > 1:
            form.base_fields['template'] = forms.ChoiceField(choices=self.plugin_templates)
        else:
            self.exclude.append('template')
            if 'template' in self.fieldsets[0][1]['fields']:
                self.fieldsets[0][1]['fields'].remove('template')
        return form

    @classmethod
    def render_post(cls, post=None, slug=None, instance=None):
        if not post:
            post = Post.objects.get(slug=slug)
        context = {'post': post.dict()}
        if instance:
            context.update(instance.get_fields_dict())
        return render_to_string(cls.plugin_post_template, context)

    def render(self, context, instance, placeholder):
        extra_context = {}
        # use template from the instance if provided
        if instance and instance.template:
            self.render_template = instance.template
        extra_context['plugin_id'] = instance.id
        # get filters and single post if requested
        if 'request' in context:
            request = context['request']
            slug = request.GET.get('post')
            plugin_filters = request.GET.get('plugin_%s_filters' % instance.id)
            global_plugin_filters = request.GET.get('plugin_filters')
        else:
            slug = plugin_filters = global_plugin_filters = None
        if slug:
            # get single post
            extra_context['post'] = instance.get_post(slug)
        filters = {}
        if plugin_filters:
            # get plugin filters
            for param in plugin_filters.split('|'):
                [key, value] = param.split('=')
                filters[key] = value
        if global_plugin_filters:
            # get plugin filters
            for param in global_plugin_filters.split('|'):
                [key, value] = param.split('=')
                filters[key] = value
        extra_context['filters'] = filters
        # get plugin posts
        extra_context['posts'] = instance.get_posts(filters=filters)
        # get plugin attributes
        extra_context.update(instance.get_fields_dict())
        # add debug for development
#        extra_context['debug'] = simplejson.dumps(extra_context, indent=4)
        # setup a paginator
        limit = int(filters.get('limit', instance.__dict__.get('page_size', 0)))
        if limit:
            paginator = Paginator(extra_context['posts'], limit)
            current_page = filters.get('page', 1)
            try:
                page = paginator.page(current_page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                page = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                page = paginator.page(paginator.num_pages)
            extra_context['paginator'] = paginator
            extra_context['page'] = extra_context['posts'] = page
        # return updated context
        context.update(extra_context)
        context.update(self._extra_context(context, instance))
        return context

    def _extra_context(self, context, instance):
        """ Adds extra context for rendering

        Args:
         * context - original context prepared by default render method

        Override it if you want to add anything to the context before rendering.

        Returns a dictionary with additional context values.
        """
        return {}