# -*- coding: utf-8 -*-

import datetime
import hashlib

from django.utils import simplejson

from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.utils.translation import ugettext as _
from django.core.cache import cache

import unidecode

from django.template import defaultfilters
from goscale import conf



class Post(models.Model):
    link = models.URLField(blank=True, null=True, db_index=True) # link is also unique identifier for each entry
    permalink = models.CharField(max_length=250, blank=True, null=True, db_index=True) # page independent permalink
    content_type = models.CharField(max_length=250, blank=True, null=True, db_index=True) # MIME type for data field
    slug = models.CharField(max_length=250, blank=True, null=True, db_index=True) #short title, text without HTML
    updated = models.DateTimeField(blank=True, null=True, db_index=True)  # last updated
    published = models.DateTimeField(blank=True, null=True, db_index=True) #pubDate
    title = models.CharField(max_length=250, blank=True, null=True) #short title, text without HTML
    description = models.TextField(blank=True, null=True) #universal text/html representation of entry
    author = models.CharField(max_length=250, blank=True, null=True)
    categories = models.CharField(max_length=250, blank=True, null=True, db_index=True)
    summary = models.TextField(blank=True, null=True) #short plain text description
    attributes = models.TextField(blank=True, null=True) #JSON

    def save(self, **kw):
        self.set_slug()  # handle slug
        self.set_links() # handle links
        self.format_categories()
        super(Post, self).save(**kw) # handle links

    def set_slug(self, slug=None):
        if slug:
            self.slug = slug
            return
        if self.title:
            self.slug = defaultfilters.slugify(unidecode.unidecode(self.title))
        else:
            self.slug = str(self.id)
        return

    def set_links(self, permalink=None):
        if permalink:
            self.permalink = permalink
        else:
        #            self.permalink = '/posts/%s/' % self.slug
            self.permalink = self.link
        return

    def format_categories(self):
        if self.categories:
            self.categories = ','.join(['[%s]' % tag.strip(' ') for tag in self.categories.split(',')])
        return

    def json(self):
        post_dict = {
            'id': self.id,
            'link': self.link,
            'permalink': self.permalink,
            'content_type': self.content_type,
            'slug': self.slug,
            'updated': self.updated.strftime(conf.GOSCALE_ATOM_DATETIME_FORMAT),
            'published': self.published.strftime(conf.GOSCALE_ATOM_DATETIME_FORMAT),
            'title': self.title,
            'description': self.description,
            'author': self.author,
            'categories': self.categories[1:-1].split(',') if self.categories else None,
            'summary': self.summary,
            }
        if self.attributes:
            attributes = simplejson.loads(self.attributes)
            post_dict.update(attributes)
        return post_dict

    def __unicode__(self):
        return 'post object: %s' % self.title or self.id


class GoscaleCMSPlugin(CMSPlugin):
    """
    Common base abstract class for all the GoScale plugins
    """
    #    plugin_templates = PLUGIN_TEMPLATES
    # Fields
    posts = models.ManyToManyField(Post, verbose_name=_('Posts'))
    template = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Template'))
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Title'))

    # Private Attributes
    _dummy_datetime = datetime.datetime.now()
    _fields = []

    class Meta:
        abstract = True

    # Override metods
    def copy_relations(self, oldinstance):
        self.posts = oldinstance.posts.all()

    # Public methods
    def get_cache_key(self, offset=0, limit=0, order=None, post_slug=''):
        """ The return of Get
        """
        return hashlib.sha1(
            '.'.join([
                self.__module__,
                self.__class__.__name__,
                str(self._fields),
                str(offset),
                str(limit),
                str(order),
                str(post_slug),
                ])
        ).hexdigest()

    def get_posts(self, offset=0, limit=1000, order=conf.GOSCALE_DEFAULT_CONTENT_ORDER):
        """ This method returns list of Posts for this Data Source starting at a given offset and not more than limit
        It will call content-specific methods:
             _format() to format output from the DataStore
        """
        cache_key = self.get_cache_key(offset, limit, order)
        content = cache.get(cache_key)
        if content:
            return content
        self.update() #TODO: update somewhere else
        query = self._get_query()
        posts = query[offset:offset+limit]
        posts = self._format(posts)
        cache_duration = conf.GOSCALE_CACHE_DURATION if posts else 1
        cache.set(cache_key, posts, cache_duration)
        return posts

    def get_post(self, slug):
        """ This method returns a single post by slug
        """
        cache_key = self.get_cache_key(post_slug=slug)
        content = cache.get(cache_key)
        if not content:
            post = Post.objects.get(slug=slug)
            content = self._format(post)
            cache_duration = conf.GOSCALE_CACHE_DURATION if post else 1
            cache.set(cache_key, content, cache_duration)
        return content

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
            stored_entry, is_new = Post.objects.get_or_create(link=entry.link)
            self._store_post(stored_entry, entry)
            if is_new is True:
            #self._set_dates(stored_entry)
            #                self._store_post(stored_entry, entry)
                msg.append('Post "%s" added.' % entry.link)
            else:
                msg.append('Post "%s" already saved.' % entry.link)
        return '<br />'.join(msg)

    # Private methods
    def _get_data_source_url(self):
        """This method should return URL to identify Posts.
        Different content types may store the URL in a different parameters or even create a dummy one
        """
        if 'url' not in self.__dict__:
            return None
        return self.__getattribute__('url')

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

    def _get_query(self, order=conf.GOSCALE_DEFAULT_CONTENT_ORDER):
        """ This method is just to evade code duplication in count() and get_content, since they do basically the same thing"""
        return self.posts.all().order_by(order)

    def _format(self, posts):
        """ This method is called by get_content() method"""
        if posts.__class__ == Post:
            # format a single post
            return posts.json()
        formated_posts = []
        for post in posts:
            formated_posts.append(post.json())
        return formated_posts


def update_posts(**kwargs):
    plugin = kwargs['instance']
    plugin.posts.all().delete() # TODO: handle old posts deleting if source changes without deleting every time
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