# -*- coding: utf-8 -*-
from classytags.arguments import Argument, MultiValueArgument, MultiKeywordArgument
from classytags.core import Options
from classytags.helpers import InclusionTag
from django import template
from cms.templatetags import cms_tags
from cms.models import CMSPlugin
from goscale import models
from goscale import cms_plugins

register = template.Library()


class GoscalePaginator(InclusionTag):
    name = 'goscale_paginator'
    template = 'paginator.html'
    options = Options(
        MultiKeywordArgument('params', required=False)
    )

    def get_template(self, context, **kwargs):
        """
        Returns the template to be used for the current context and arguments.
        """
        if 'template' in kwargs['params']:
            self.template = kwargs['params']['template']
        return super(GoscalePaginator, self).get_template(context, **kwargs)

    def get_context(self, context, params):
        return {
            'paginator': context['paginator'],
            'page': context['page']
        }

register.tag(GoscalePaginator)

class GoscalePlaceholder(cms_tags.Placeholder):
    """
    This template node is used to output page content and
    is also used in the admin to dynamically generate input fields.

    eg: {% placeholder "placeholder_name" %}

    {% placeholder "sidebar" inherit %}

    {% placeholder "footer" inherit or %}
        <a href="/about/">About us</a>
    {% endplaceholder %}

    Keyword arguments:
    name -- the name of the placeholder
    width -- additional width attribute (integer) which gets added to the plugin context
    (deprecated, use `{% with 320 as width %}{% placeholder "foo"}{% endwith %}`)
    inherit -- optional argument which if given will result in inheriting
        the content of the placeholder with the same name on parent pages
    or -- optional argument which if given will make the template tag a block
        tag whose content is shown if the placeholder is empty
    """
    name = 'goscale_placeholder'
    options = cms_tags.PlaceholderOptions(
        Argument('name', resolve=False),
        MultiKeywordArgument('goscale', required=False),
        MultiValueArgument('extra_bits', required=False, resolve=False),
        blocks=[
            ('endplaceholder', 'nodelist'),
        ]
    )

    def render_tag(self, context, *args, **kwargs):
        if 'goscale' in kwargs:
            if 'render_posts' in kwargs['goscale']:
                if kwargs['goscale']['render_posts'].lower() == 'true':
                    if 'request' in context:
                        request = context['request']
                        slug = request.GET.get('post')
                        plugin_id = request.GET.get('plugin_id')
                        if slug:
                            if plugin_id:
                                plugin = CMSPlugin.objects.get(pk=plugin_id)
                                plugin = plugin.get_plugin_class()
                            else:
                                plugin = cms_plugins.GoscaleCMSPluginBase
                            return plugin.render_post(slug=slug)
#                            post = models.Post.objects.get(slug=slug)
#                            raise ValueError
#                            return post.json()
            if 'ajaxify' in kwargs['goscale']:
                pass # TODO: Ajaxify placeholders
#            return kwargs
            kwargs.pop('goscale')
        return super(GoscalePlaceholder, self).render_tag(context, *args, **kwargs)

register.tag(GoscalePlaceholder)