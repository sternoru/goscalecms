# -*- coding: utf-8 -*-

import datetime
import urllib2
import hashlib
import re

from django.core.cache import cache
from django.core import exceptions
from django.utils import simplejson

import feedparser

from cms.models.pluginmodel import CMSPlugin
from goscale.plugins.cms_plugins import GoscaleCMSPluginBase
from goscale import models as goscale_models
from goscale import utils
from django.db import models


class GoscaleCMSPlugin(CMSPlugin):
    """
    Common base abstract class for all the GoScale plugins
    """
    # Fields
    posts = models.ManyToManyField(goscale_models.Post, related_name='plugins')

    # Private Attributes
    _dummy_datetime = datetime.datetime.now()
    _fields = []

    class Meta:
        abstract = True

    # Override metods
    def copy_relations(self, oldinstance):
        self.posts = oldinstance.posts.all()

    # Public methods
    def get_cache_key(self, offset=0, limit=0, post_slug=''):
        """ The return of Get
        """
        return hashlib.sha1(
            '.'.join([
                self.__module__,
                self.__class__.__name__,
                str(self._fields),
                str(offset),
                str(limit),
                str(post_slug),
                ])
        ).hexdigest()

    def update(self):
        """This method should be called to update associated Posts
        It will call content-specific methods:
             _get_data() to obtain list of entries
             _store_post() to store obtained entry object
             _get_data_source_url() to get an URL to identify Posts from this Data Source
        """
        #get the raw data
        data = self._get_data()
        #iterate through them and for each item
        msg = []
        for entry in data:
            stored_entry, is_new = goscale_models.Post.objects.get_or_create(link=entry.link)
            self._store_post(stored_entry, entry)
            if is_new is True:
                #self._set_dates(stored_entry)
#                self._store_post(stored_entry, entry)
                msg.append('Post "%s" added.' % entry.link)
            else:
                msg.append('Post "%s" already saved.' % entry.link)
        return '<br />'.join(msg)

    # Private methods
    def _get_dummy_datetime(self):
        """ This method is to store posts which have no publish date.
        Please note that post retrieved later will have an earlier publication date - just as it is in RSS feeds.
        """
        self._dummy_datetime -= datetime.datetime.resolution
        return self._dummy_datetime

    def _get_data(self):
        """ Gets raw data from data source. Returns list of dictionaries
        basically, request a http  or google data
        check hash of response and return [] if feed not changed
        cash response hash for further comparison
        split to entries and return array """
        return []

    def _store_post(self, stored_entry, entry=None):
        """ This method formats entry returned by _get_data() and puts to DB
        create textDesc, title, and MIME """
#        stored_entry.content_type = utils.get_source_setting(ds.type, 'type')
        if stored_entry.published is None:
            stored_entry.published = self._get_dummy_datetime()
        if stored_entry.updated is None:
            stored_entry.updated = self._get_dummy_datetime()
#        print 'Post: %s' % stored_entry.title
#        print 'Attributes: %s' % stored_entry.attributes
        stored_entry.save()
        self.posts.add(stored_entry)
        return None


def update_posts(**kwargs):
    plugin = kwargs['instance']
    plugin.update()


class WrongAttribute(Exception):
    def __init__(self, message=None, attribute=None):
        if not message:
            if attribute is not None:
                message = 'Attribute "%s" has wrong format' % attribute
            else:
                message = 'Attribute has wrong format'
        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)
