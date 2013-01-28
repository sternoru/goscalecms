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


class VideosBase(goscale_models.GoscaleCMSPlugin):
    """
    YouKu Videos
    """
    playlist = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Playlist'),
        help_text='Playlist URL')
    lightbox = models.BooleanField(default=False, verbose_name=_('Open videos in a lightbox'),
        help_text=_('If checked videos will open in a lightbox, otherwise inline.'))

    class Meta:
        abstract = True


class YouKu(VideosBase):
    """
    YouKu Videos
    """
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

YouKu._meta.get_field('playlist').help_text = 'ex: http://www.youku.com/playlist_show/id_17031624.html'
YouKu._meta.get_field('playlist').verbose_name = _('Youku playlist')

signals.post_save.connect(goscale_models.update_posts, sender=YouKu)


class Youtube(VideosBase):
    """
    Youtube videos
    """
    channel = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('Youtube channel'),
        help_text='ex: https://www.youtube.com/user/GoogleDevelopers')

    def _regex_id(self, url=None):
        id = None
        try:
            url = url or self.playlist
            id = re.search('(list=)([\d\w._]+)', url).group(2)
        except AttributeError:
            try:
                url = url or self.channel
                id = re.search('(\/user\/)([\d\w+._]+)', url).group(2)
            except AttributeError:
                raise goscale_models.WrongAttribute(attribute='channel')
        if not id:
            raise goscale_models.WrongAttribute(attribute='playlist')
        return id

    def _get_data_source_url(self):
        if self.playlist:
            # try youtube_playlist.
            id = self._regex_id(self.playlist)
            url = 'http://www.youtube.com/view_play_list?p=%s' % id
        elif self.channel:
            # youtube_channel
            id = self._regex_id(self.channel)
            url = 'http://www.youtube.com/user/%s' % id
        else:
            url = None
        return url

    def _get_data(self):
        from gdata.youtube import service
        try:
            video_service = service.YouTubeService()
            if self.channel:
                # youtube_channel
                query = service.YouTubeVideoQuery()
                query.author = self._regex_id(self.channel)
                query.orderby = 'published'
                feed = video_service.YouTubeQuery(query)
            elif self.playlist:
                # if not youtube_channel, then it's youtube_playlist.
                playlist = self._regex_id(self.playlist)
                feed = video_service.GetYouTubePlaylistVideoFeed(uri='http://gdata.youtube.com/feeds/api/playlists/%s?orderby=published' % playlist)
            return feed.entry
        except:
            return []

    def _store_post(self, stored_entry, entry):
        video_id = entry.link[0].href.replace('http://www.youtube.com/watch?v=', '').split('&')[0]
        if entry.rating and entry.rating.average:
            entry_rating = int(round(float(entry.rating.average)*10))
            if entry_rating%5 > 2:
                video_rating = entry_rating - (entry_rating%5) + 5
            else:
                video_rating = entry_rating - (entry_rating%5)
        else:
            video_rating = 0

        if entry.statistics and entry.statistics.view_count:
            video_view_count = int(entry.statistics.view_count)
        else:
            video_view_count = 0
        stored_entry.title = unicode(entry.title.text, "utf-8")
        stored_entry.author = unicode(entry.author[0].name.text, "utf-8")
        stored_entry.categories = entry.media.category[0].text
        stored_entry.attributes = simplejson.dumps({
            'id': video_id,
            'author_url': 'http://youtube.com/profile?user=%s' % entry.author[0].name.text,
            'thumbnail': 'http://i.ytimg.com/vi/%s/2.jpg' % video_id,
            'video_url': 'http://www.youtube.com/v/%s&hl=en&fs=1' % video_id,
            'rating': video_rating,
            'view_count': video_view_count
        })
        return super(Youtube, self)._store_post(stored_entry)

Youtube._meta.get_field('playlist').help_text = 'ex: https://www.youtube.com/watch?v=tV7IhJwU3hA&list=PL53B883EBFFAE300C'
Youtube._meta.get_field('playlist').verbose_name = _('YouTube playlist')

signals.post_save.connect(goscale_models.update_posts, sender=Youtube)


class Vimeo(VideosBase):
    """
    Vimeo videos
    """
    user = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('Vimeo user'),
        help_text='ex: http://vimeo.com/amandanedermeijer')

    def _regex_id(self, url=None):
        id = None
        try:
            url = url or self.playlist
            id = re.search('(\/channels\/)([\d\w._]+)', url).group(2)
        except AttributeError:
            try:
                url = url or self.user
                id = re.search('(vimeo.com/)([\d\w+._]+)', url).group(2)
            except AttributeError:
                raise goscale_models.WrongAttribute(attribute='user')
        if not id:
            raise goscale_models.WrongAttribute(attribute='playlist')
        return id

    def _get_data_source_url(self):
        if self.playlist:
            id = self._regex_id(self.playlist)
            url = 'http://vimeo.com/channels/%s' % id # vimeo channel  http://vimeo.com/channels/...
        elif self.user:
            id = self._regex_id(self.user)
            url = 'http://vimeo.com/%s' % id # vimeo user  http://vimeo.com/...
        else:
            url = None
        return url

    def _get_data(self):
        try:
            if self.playlist:
                id = self._regex_id(self.playlist) # http://vimeo.com/channels/iphonehd
                feed_url = 'http://vimeo.com/api/v2/channel/%s/videos.json' % id
            elif self.user:
                id = self._regex_id(self.user) # http://vimeo.com/wyldstallyons
                feed_url = 'http://vimeo.com/api/v2/%s/videos.json' % id
            req = utils.forge_request(feed_url.encode('utf-8'))
            json = urllib2.urlopen(req).read()
            feed = simplejson.loads(json)
            # jsonfeed is a list of dictionaries
            # For update(), we need a list of objects. transforming the feed below.
            data = []
            for entry in feed:
                entry['link'] = entry['url']
                data.append(utils.dict2obj(entry))
            return data
        except:
            raise
            return []

    def _store_post(self, stored_entry, entry):
        stored_entry.title = entry.title
        stored_entry.author = entry.user_name
        stored_entry.categories = entry.tags
        stored_entry.published = entry.upload_date
        stored_entry.attributes = simplejson.dumps({
            'id': entry.id,
            'comments_id': entry.id,
            'description': entry.description,
            'author_url': entry.user_url,
            'thumbnail': entry.thumbnail_medium,
            'video_url':  'http://vimeo.com/moogaloop.swf?clip_id=%s&amp;server=vimeo.com&amp;fullscreen=1&amp;show_title=1&amp;show_byline=1&amp;show_portrait=1&amp;color=00ADEF' % entry.id,
#            'likes_count': entry.stats_number_of_likes,
#            'view_count': entry.stats_number_of_views,
#            'comments_count': entry.stats_number_of_comments,
            })
        return super(Vimeo, self)._store_post(stored_entry)

Vimeo._meta.get_field('playlist').help_text = 'ex: http://vimeo.com/channels/6513'
Vimeo._meta.get_field('playlist').verbose_name = _('Vimeo channel')

signals.post_save.connect(goscale_models.update_posts, sender=Vimeo)