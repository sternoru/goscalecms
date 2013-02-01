# -*- coding: utf-8 -*-
import simplejson
import urllib
from classytags.arguments import Argument, MultiValueArgument, MultiKeywordArgument
from classytags.core import Options
from classytags.helpers import InclusionTag, AsTag
from django import template
from cms.templatetags import cms_tags
from cms.models import CMSPlugin
from sekizai.templatetags import sekizai_tags
from goscale import models
from goscale import cms_plugins

register = template.Library()


class Paginator(InclusionTag):
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
        return super(Paginator, self).get_template(context, **kwargs)

    def get_context(self, context, params):
        paginator = context['paginator']
        page = context['page']
        page_range = []
        if len(paginator.page_range) > 6:
            page_range.extend(paginator.page_range[:5])
            if page.number > 5:
                if page.number > 7:
                    page_range.append('...')
                if page.number == 6:
                    page_range.extend(paginator.page_range[(page.number-1):(page.number+1)])
                else:
                    page_range.extend(paginator.page_range[(page.number-2):(page.number+1)])
            elif page.number == 5:
                page_range.append(6)
            if len(paginator.page_range) - page.number > 2:
                page_range.append('...')
            if len(paginator.page_range) - page.number > 1:
                page_range.append(paginator.page_range[-1])
        else:
            page_range = paginator.page_range
        context['page_range'] = page_range
        return context

register.tag(Paginator)


class PluginFilters(AsTag):
    name = 'goscale_plugin_filters'
    options = Options(
        MultiKeywordArgument('params', required=False),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, params):
        filters = []
        is_global = params.pop('global') if 'global' in params else ''
        is_exclusive = params.pop('exclusive') if 'exclusive' in params else ''
        if is_global.lower() in ['true', 'yes']:
            plugin_filters = 'plugin_filters'
        else:
            plugin_filters = 'plugin_%s_filters' % context['plugin_id']
        for key, val in params.iteritems():
            filters.append('='.join([key, str(val)]))
        qs = ['='.join([plugin_filters, '|'.join(filters)])]
        if is_exclusive.lower() not in ['true', 'yes']:
            for key, value in context['request'].GET.iteritems():
                if key.startswith('_') or key == plugin_filters:
                    continue
                qs.append('='.join([key, value]))
        return '?' + '&'.join(qs)

register.tag(PluginFilters)


class PluginPost(AsTag):
    name = 'goscale_plugin_post'
    options = Options(
        Argument('post'),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, post):
        return '?post=%s&plugin_id=%s' % (post['slug'], context['plugin_id'])

register.tag(PluginPost)


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
                                instance = plugin.get_plugin_instance()[0]
                                plugin = plugin.get_plugin_class()
                            else:
                                instance = None
                                plugin = cms_plugins.GoscaleCMSPluginBase
                            return plugin.render_post(slug=slug, instance=instance)
#                            post = models.Post.objects.get(slug=slug)
#                            raise ValueError
#                            return post.json()
            if 'ajaxify' in kwargs['goscale']:
                pass # TODO: Ajaxify placeholders
#            return kwargs
            kwargs.pop('goscale')
        return super(GoscalePlaceholder, self).render_tag(context, *args, **kwargs)

register.tag(GoscalePlaceholder)


class GoscaleAddtoBlock(sekizai_tags.Addtoblock):
    name = 'goscale_addtoblock'

    def render_tag(self, *args, **kwargs):
        from django import http
        context = args[0]
        request = context.get('request')
        if request and (request.is_ajax() or 'ajax' in request.GET):
            return nodelist.render(context)
        return super(GoscaleAddtoBlock, self).render_tag(*args, **kwargs)

register.tag(GoscaleAddtoBlock)