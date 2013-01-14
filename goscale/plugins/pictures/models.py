import re
import os
import simplejson
import datetime
import urllib2
from gdata.photos import service
from goscale import models as goscale_models
from goscale import utils
from goscale import conf
from goscale import decorators
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext as _


class Picasa(goscale_models.GoscaleCMSPlugin):
    """
    Picasa photos
    """
    url = models.CharField(max_length=250, verbose_name=_('Picasa user or album link'),
        help_text=_('user: https://plus.google.com/photos/114610201247248895941/<br/> \
            album: https://plus.google.com/photos/114610201247248895941/albums/5319044261264143137<br/> \
            picasaweb album (RSS link): https://picasaweb.google.com/data/feed/base/user/sterno.bloggerCMS/albumid/5352591675044168945?alt=rss&kind=photo&hl=en_US'))
    width = models.SmallIntegerField(null=True, blank=True, verbose_name=_('Container width'),
        help_text=_('Width of a slideshow container or a lightbox.'))
    height = models.SmallIntegerField(null=True, blank=True, verbose_name=_('Container height'),
        help_text=_('Height of a slideshow container or a lightbox.'))
    thumbnail_width = models.SmallIntegerField(null=True, blank=True, verbose_name=_('Thumbnail width'),
        help_text=_('Width of a thumbnail.'))
    thumbnail_height = models.SmallIntegerField(null=True, blank=True, verbose_name=_('Thumbnail height'),
        help_text=_('Height of a thumbnail.'))
    autoplay = models.BooleanField(default=False, verbose_name=_('Autoplay'),
        help_text=_('If set slideshow will start automatically.'))
    user = None
    album = None
    type = 'photos'

    def _regex_id(self, url=None):
        if not url:
            url = self.url
        id = None
        try:
            # check for album (picasaweb style)
            match = re.search('(\/user\/)([\d\w.]+)(\/albumid\/)(\d+)', url)
            id = match.group(4)
            self.album = id
            self.user = match.group(2)
            return id
        except AttributeError:
            pass
        try:
            # check for album (google+ style)
            match = re.search('(\/photos\/)([\d\w.]+)(\/albums\/)(\d+)', url)
            id = match.group(4)
            self.album = id
            self.user = match.group(2)
            return id
        except AttributeError:
            pass
        try:
            # check for user
            id = re.search('(\/photos\/)([\d\w.]+)(\/)', url).group(2)
            self.user = id
            if not self.album:
                self.type = 'albums'
            return id
        except AttributeError:
            raise goscale_models.WrongAttribute(attribute='url')
        return id

    def _get_entry_link(self, entry):
        """ Returns a unique link for an entry
        """
        entry_link = None
        for link in entry.link:
            if '/data/' not in link.href and '/lh/' not in link.href:
                entry_link = link.href
                break
        return entry_link or entry.link[0].href

    def _get_data(self, album_id=None):
        data = []
        id = self._regex_id()
        if self.type == 'photos':
            # type photo with album_id
            album_id = album_id or self.album
            data = self._get_picasa_photos(album_id)
#        elif type == 'photos':
#            # type photo without album_id
#            for album_id in self.params.get('albums', None):
#                data.extend(self._get_picasa_photos(album_id))
        elif self.type == 'albums':
            # type album or all: (in either case, we need to get the albums.)
            albums = self._get_picasa_albums()
#            data.extend(albums)
            print 'user: %s' % self.user
            for album in albums:
                print 'album: %s' % album.gphoto_id.text
                data.extend(self._get_picasa_photos(album.gphoto_id.text))
        return data

    def _store_post(self, stored_entry, entry=None):
        """ This method formats entry returned by _get_data() and puts to DB
        create textDesc, title, and MIME """
        stored_entry.content_type = self.type
        if 1==1 or self.type == 'photos': # ignore type for now
            # is photo
            width = int(entry.width.text)
            height = int(entry.height.text)
            orientation = 'landscape' if width > height else 'portrait'
            max = width if width > height else height
            thumbnails = {}
            sizes = ['72', '144', '288', '480', '512', '800', '1200', '1600']
            for thumb in entry.media.thumbnail:
                size = thumb.width if width > height else thumb.height
                thumbnails['s%s' % size] = {
                    'url': thumb.url,
                    'height': thumb.height,
                    'width': thumb.width
                }
            for size in sizes[3:]:
                big = size
                small = str(int(int(size)/(float(72)/float(thumbnails['s72']['height' if width > height else 'width']))))
                thumbnails['s%s' % size] = {
                    'url': thumbnails['s72']['url'].replace('s72', 's%s' % size),
                    'height': big if height > width else small,
                    'width': small if height > width else big
                }
            url = thumbnails['s144']['url'].replace('s144', 's%s' % max)
            stored_entry.link = self._get_entry_link(entry)
            summarytext = ''
            if entry.summary.text != None:
                summarytext = unicode(entry.summary.text, "utf-8")
            stored_entry.summary = summarytext
            stored_entry.title = unicode(entry.title.text, "utf-8")
            stored_entry.categories = 'photos'
            stored_entry.published = datetime.datetime.strptime(entry.published.text, '%Y-%m-%dT%H:%M:%S.%fZ')
            stored_entry.updated = datetime.datetime.strptime(entry.updated.text, '%Y-%m-%dT%H:%M:%S.%fZ')
            stored_entry.author = entry.albumid.text
            stored_entry.attributes = simplejson.dumps({
                'id': entry.gphoto_id.text,
                'thumbnails': thumbnails,
                'url': url,
                'width': str(width),
                'height': str(height),
                'orientation': orientation
            })
#        elif self.type == 'albums':
#            # is albums
#            summarytext = ''
#            if entry.summary.text != None:
#                summarytext = unicode(entry.summary.text, "utf-8")
#            itemLink = entry.link[1].href
#            stored_entry.name = itemLink[itemLink.rfind('/')+1:]
#            stored_entry.categories = 'albums'
#            stored_entry.title = unicode(entry.title.text, "utf-8")
#            stored_entry.published = datetime.datetime.strptime(entry.published.text, '%Y-%m-%dT%H:%M:%S.%fZ')
#            stored_entry.updated = datetime.datetime.strptime(entry.updated.text, '%Y-%m-%dT%H:%M:%S.%fZ')
#            stored_entry.author = entry.user.text
#            stored_entry.summary = summarytext
#            stored_entry.attributes = simplejson.dumps({
#                'id': entry.gphoto_id.text,
#                'thumbnail': entry.media.thumbnail[0].url,
#        })
        return super(Picasa, self)._store_post(stored_entry)

    @decorators.cache_func
    def _get_picasa_albums(self):
        # get albums by user
        try:
            result = []
            gd_client = service.PhotosService()
            albums = gd_client.GetUserFeed(user=self.user)
            for album in albums.entry:
                result.append(album)
            return result
        except:
            raise
            return []

    @decorators.cache_func
    def _get_picasa_photos(self, album_id):
        # get photos by album_id
        try:
            gd_client = service.PhotosService()
            photos = gd_client.GetFeed('/data/feed/api/user/%s/albumid/%s?kind=photo' % (self.user, album_id))
            return photos.entry
        except:
            raise
            return []

#signals.post_save.connect(goscale_models.update_posts, sender=Picasa)