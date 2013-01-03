# -*- coding: utf-8 -*-

import unidecode

from django.db import models
from django.template import defaultfilters
from django.utils import simplejson
from django.utils.translation import ugettext as _
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