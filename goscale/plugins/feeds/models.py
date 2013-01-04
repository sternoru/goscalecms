import re
import feedparser
import urllib2
import simplejson
import datetime
from goscale import models as goscale_models
from goscale import utils
from goscale import conf
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext as _


class Feed(goscale_models.GoscaleCMSPlugin):
    """
    RSS Feed posts
    """
    url = models.URLField(max_length=250, verbose_name=_('Feed URL'),
        help_text='ex: http://feeds.bbci.co.uk/news/technology/rss.xml')
    page_size = models.PositiveSmallIntegerField(default=conf.GOSCALE_DEFAULT_PAGE_SIZE,
        verbose_name=_('Posts per page'), help_text=_('set 0 for unlimited.'))
    show_date = models.BooleanField(default=False, verbose_name=_('Show date in posts'),
        help_text=_('If checked the date will be shown along with the post content.'))

    def _get_data(self):
        url = self._get_data_source_url()
        if not url:
            return []
        res = urllib2.urlopen(url.encode('utf-8'))
        #TBD get hash and compare to cache value
        feed = feedparser.parse(res.read())
        return feed.entries

    def _store_post(self, stored_entry, entry):
        stored_entry.content_type = 'text/html'

        updated_tz_delta = 0
        updated_string = entry.get('updated') or entry.get('published')
        updated_tz_delta = utils.process_feed_tz_delta(updated_string)

        published_tz_delta = 0
        published_string = entry.get('published') or entry.get('updated')
        published_tz_delta = utils.process_feed_tz_delta(published_string)

        stored_entry.updated = utils.get_datetime_by_parsed(entry.get('updated_parsed') or entry.get('published_parsed'), updated_tz_delta)
        stored_entry.published = utils.get_datetime_by_parsed(entry.get('published_parsed') or entry.get('updated_parsed'), published_tz_delta)
        stored_entry.title = entry.get('title')
        content = entry.get('summary')
        if not content:
            content_list = entry.get('content')
            for content_item in content_list:
                content = content_item.get('value') or content_item
        stored_entry.description = content
        stored_entry.summary = utils.get_short_summary(content)
        stored_entry.author = entry.get('author')
        if entry.get('tags'):
            stored_entry.categories = ','.join([tag.get('term') or tag.get('label') for tag in entry.get('tags') if tag.get('term') or tag.get('label')])
            #other stuff we might need
        author_details = entry.get('author_detail')
        if author_details:
            stored_entry.attributes = simplejson.dumps(dict(author_details=author_details))
            #stored_entry.author
        return super(Feed, self)._store_post(stored_entry)

signals.post_save.connect(goscale_models.update_posts, sender=Feed)