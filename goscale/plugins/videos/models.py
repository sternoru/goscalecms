import re
import feedparser
import urllib2
import simplejson
import datetime
from goscale import models as goscale_models
from goscale import utils
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext as _


class YouKu(goscale_models.GoscaleCMSPlugin):
    """
    YouKu Videos
    """
    playlist = models.CharField(max_length=250, verbose_name=_('Youku playlist'),
        help_text='ex: http://www.youku.com/playlist_show/id_17031624.html')
    lightbox = models.BooleanField(default=False, verbose_name=_('Open videos in a lightbox'),
        help_text=_('If checked videos will open in a lightbox, otherwise inline.'))

    def _regex_id(self, link=None):
        link = link or self.playlist
        try:
            # this regex can also handle unicode encoded characters in the id.
            return re.match(r'(http://)?(u.|www.)?(youku.com/)?(playlist_show/id_|user_show/uid_)?((.+)[^\.html])', link).group(5)
        except AttributeError:
            raise goscale_models.WrongAttribute(attribute='playlist')

    def _get_data_source_url(self):
        if self.playlist:
            id = self._regex_id(self.playlist)
            return 'http://www.youku.com/playlist_show/id_%s' % id
        return ''

    def _get_data(self):
        try:
            if self.playlist:
                id = self._regex_id(self.playlist) # http://www.youku.com/playlist/rss/id/ + id
                feed_url = 'http://www.youku.com/playlist/rss/id/%s' % id
                req = utils.forge_request(feed_url.encode('utf-8'))
                rss = urllib2.urlopen(req).read()
                feed = feedparser.parse(rss)
                data = []
                for entry in feed.entries:
                    data.append(utils.dict2obj(entry))
                return data
        except:
            pass
        return []

    def _store_post(self, stored_entry, entry):
        video_id = entry.link.replace('http://www.youku.com/v_show/id_', '').split('_')[0]
        arr = entry.summary.split(' src="')
        if len(arr) == 1:
            thumbnail = None
        else:
            thumbnail = arr[1].split('"')[0]
        try:
            datetime_obj = datetime.datetime.strptime(entry.updated[0:-6], "%a, %d %b %Y %H:%M:%S") # Sun, 26 Apr 2009 00:45:30
            stored_entry.published = datetime_obj - datetime.timedelta(minutes=480) #convert to GMT
        except:
            stored_entry.published = None
        stored_entry.title = entry.title
        stored_entry.author = entry.author
        stored_entry.category = entry.itunes_keywords
        stored_entry.summary = entry.summary
        video_url = ''
        for link in entry.links:
            if link.rel == 'enclosure':
                video_url = link.href
        stored_entry.attributes = simplejson.dumps({
            'video_id': video_id,
            'thumbnail': thumbnail,
            'video_url': video_url,
            })
        return super(YouKu, self)._store_post(stored_entry)

signals.post_save.connect(goscale_models.update_posts, sender=YouKu)