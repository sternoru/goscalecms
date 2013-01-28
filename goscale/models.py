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
from goscale import conf, utils


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

    def dict(self):
        """ Returns dictionary of post fields and attributes
        """
        post_dict = {
            'id': self.id,
            'link': self.link,
            'permalink': self.permalink,
            'content_type': self.content_type,
            'slug': self.slug,
            'updated': self.updated, #.strftime(conf.GOSCALE_ATOM_DATETIME_FORMAT),
            'published': self.published, #.strftime(conf.GOSCALE_ATOM_DATETIME_FORMAT),
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

    def json(self, dict=None, indent=None):
        """ Returns post JSON representation
        """
        if not dict:
            dict = self.dict()
        for key, value in dict.iteritems():
            if type(value) == datetime.datetime:
                dict[key] = value.strftime(conf.GOSCALE_ATOM_DATETIME_FORMAT)
        return simplejson.dumps(dict, indent=indent)

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
    updated = models.DateTimeField(blank=True, null=True, db_index=True, verbose_name=_('Last updated'))

    # Private Attributes
    _dummy_datetime = utils.get_datetime_now()
    _fields = []

    class Meta:
        abstract = True

    def __unicode__(self):
        template = self.template.replace('.html', '').capitalize() if self.template else None
        title = self.title or template or str(self.id)
        if len(title) > 25:
            title = '%s...' % title[:25]
        return title

    # Override metods
    def copy_relations(self, oldinstance):
        self.posts = oldinstance.posts.all()

    # Public methods
    @classmethod
    def get_fields_list(cls):
        fields_list = []
        ignore_fields = ['changed_date', 'cmsplugin', 'cmsplugin_ptr', 'creation_date', 'id', 'language', 'level',
                         'lft', 'parent', 'placeholder', 'plugin_type', 'position', 'posts', 'rght', 'tree_id']
        for field in cls._meta.get_all_field_names():
            if field not in ignore_fields:
                fields_list.append(field)
        return fields_list

    def get_fields_dict(self):
        fields_dict = {}
        for field in self.__class__.get_fields_list():
            value = self.__getattribute__(field)
            if field == 'updated':
                value = str(value)
            fields_dict[field] = value
        return fields_dict

    def get_cache_key(self, offset=0, limit=0, order=None, post_slug=''):
        """ The return of Get
        """
        return hashlib.sha1(
            '.'.join([
                str(self._get_data_source_url()),
                str(offset),
                str(limit),
                str(order),
                str(post_slug),
                ])
        ).hexdigest()

    def get_posts(self, offset=0, limit=1000, order=None, filters=None):
        """ This method returns list of Posts for this Data Source starting at a given offset and not more than limit
        It will call content-specific methods:
             _format() to format output from the DataStore
        """
        order = self._get_order(order)
        cache_key = self.get_cache_key(offset, limit, order, filters)
        content = cache.get(cache_key)
#        if content:
#            return content
        try:
            if self.up_to_date():
                pass # not time to update yet
            else:
                self.update()
        except:
            raise
            pass # query the database for now and update later
        query = self._get_query(order=order, filters=filters)
        posts = query[int(offset):int(offset)+int(limit)]
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

    def up_to_date(self):
        """ Returns True if plugin posts are up to date

        Determined by self.updated and conf.GOSCALE_POSTS_UPDATE_FREQUENCY
        """
#        return False
        if not self.updated:
            return False
        return (utils.get_datetime_now() - self.updated).seconds < conf.GOSCALE_POSTS_UPDATE_FREQUENCY

    def update(self):
        """This method should be called to update associated Posts
        It will call content-specific methods:
             _get_data() to obtain list of entries
             _store_post() to store obtained entry object
             _get_data_source_url() to get an URL to identify Posts from this Data Source
        """
        #get the raw data
#        self.posts.all().delete() # TODO: handle in update_posts if source changes without deleting every time
        data = self._get_data()
        #iterate through them and for each item
        msg = []
        for entry in data:
            link = self._get_entry_link(entry)
            stored_entry, is_new = Post.objects.get_or_create(link=link)
            self._store_post(stored_entry, entry)
            if is_new is True:
            #self._set_dates(stored_entry)
            #                self._store_post(stored_entry, entry)
                msg.append('Post "%s" added.' % link)
            else:
                msg.append('Post "%s" already saved.' % link)
        self.updated = utils.get_datetime_now()
        self.save(no_signals=True)
        return '<br />'.join(msg)

    # Private methods
    def _get_data_source_url(self):
        """This method should return URL to identify Posts.
        Different content types may store the URL in a different parameters or even create a dummy one
        """
        if 'url' not in self.__dict__:
            return None
        return self.__getattribute__('url')

    def _get_entry_link(self, entry):
        """ Returns a unique link for an entry

        Most likely an external link from the original source.
        Override it if you need to alter an original link or generate your own.
        """
        return entry.link

    def _get_dummy_datetime(self):
        """ This method is to store posts which have no publish date.
        Please note that post retrieved later will have an earlier publication date - just as it is in RSS feeds.
        """
#        self._dummy_datetime -= datetime.datetime.resolution
        return self._dummy_datetime

    def _get_data(self):
        """ Gets raw data from data source. Returns list of dictionaries
        basically, request a http  or google data
        check hash of response and return [] if feed not changed
        cash response hash for further comparison
        split to entries and return array """
        return []

    def _get_order(self, order=None):
        if order:
            return order
        try:
            return self.__getattribute__('order')
        except AttributeError:
            return conf.GOSCALE_DEFAULT_CONTENT_ORDER

    def _get_query(self, order=None, filters=None):
        """ This method is just to evade code duplication in count() and get_content, since they do basically the same thing"""
        order = self._get_order(order)
        return self.posts.all().order_by(order)

    def _format(self, posts):
        """ This method is called by get_content() method"""
        if posts.__class__ == Post:
            # format a single post
            return posts.dict()
        formated_posts = []
        for post in posts:
            formated_posts.append(post.dict())
        return formated_posts

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
    plugin.posts.all().delete() # TODO: handle in update_posts if source changes without deleting every time
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