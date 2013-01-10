import simplejson

from django import forms
from cms.plugin_base import CMSPluginBase
from goscale.models import GoscaleCMSPlugin, Post
from goscale import conf
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.loader import render_to_string
from django.template.context import Context

class GoscaleCMSPluginBase(CMSPluginBase):
    """
    Base class for GoScale plugins
    """
    exclude = ['posts',]
    plugin_post_template = conf.GOSCALE_DEFAULT_POST_PLUGIN
    plugin_templates = None

    def get_form(self, *args, **kwargs):
        form = super(GoscaleCMSPluginBase, self).get_form(*args, **kwargs)
        if self.plugin_templates:
            form.base_fields['template'] = forms.ChoiceField(choices=self.plugin_templates)
            print form.base_fields['template'].choices
        else:
            self.exclude.append('template')
        return form

    @classmethod
    def render_post(cls, post=None, slug=None):
        if not post:
            post = Post.objects.get(slug=slug)
        return render_to_string(cls.plugin_post_template, {'post': post.json()})

    def render(self, context, instance, placeholder):
        extra_context = {}
        # use template from the instance if provided
        if instance and instance.template:
            self.render_template = instance.template
        # get plugin posts
        extra_context['plugin_id'] = instance.id
        extra_context['posts'] = instance.get_posts()
        # get single post if requested
        slug = context['request'].GET.get('post') if 'request' in context else None
        if slug:
            extra_context['post'] = instance.get_post(slug)
        # get plugin attributes
        extra_context.update(instance.get_fields_dict())
        # add debug for development
        extra_context['debug'] = simplejson.dumps(extra_context, indent=4)
        # setup a paginator
        limit = int(context['request'].GET.get('limit', instance.__dict__.get('page_size', 0)))
        if limit:
            paginator = Paginator(extra_context['posts'], limit)
            current_page = context['request'].GET.get('page', 1)
            try:
                page = paginator.page(current_page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                page = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                page = paginator.page(paginator.num_pages)
            extra_context['paginator'] = paginator
            extra_context['page'] = page
        # return updated context
        context.update(extra_context)
        return context