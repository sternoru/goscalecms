import re
import simplejson
import datetime
import urllib2

from BeautifulSoup import BeautifulSoup
from goscale import models as goscale_models
from goscale import utils
from goscale import conf
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext as _


RATIO_CHOICES = (
    ('4:3', _('4:3 (screen)')),
    ('16:9', _('16:9 (widescreen)')),
    ('1.4142:1', _('A4 (paper, PDF)')),
)

class Presentation(goscale_models.GoscaleCMSPlugin):
    """
    Presentation Base Class
    """
    embed = models.TextField(verbose_name=_('Embed code'), help_text=_('From the "</> Embed" link.'))
    width = models.SmallIntegerField(null=True, blank=True, verbose_name=_('Width'),
        help_text=_('Width of a presentation container.'))
    height = models.SmallIntegerField(null=True, blank=True, verbose_name=_('Height'),
        help_text=_('Height of a presentation container.'))
    ratio = models.CharField(max_length=50,
        default=RATIO_CHOICES[0][0], choices=RATIO_CHOICES, verbose_name=_('Aspect ratio'),
        help_text=_('Ratio of width:height used for the presentation if manual size isn\'t set.'))
    embed_as_is = models.BooleanField(default=False, verbose_name=_('Embed "as is"'),
        help_text=_('If set embed code will not be changed.'))

    class Meta:
        abstract = True

    def save(self, no_signals=False, *args, **kwargs):
        if not self.embed_as_is:
            self.embed = self._get_embed_code()
        super(Presentation, self).save(no_signals=no_signals, *args, **kwargs)

    def _get_data(self):
        return []

    def _get_embed_code(self):
        return self.embed

    def _get_size(self, default_width=480, extra_height=61):
        ratio = [float(side) for side in self.ratio.split(':')]
        width = self.width or default_width
        height = self.height or int((width / ratio[0]) * ratio[1]) + extra_height
        return width, height

#signals.post_save.connect(goscale_models.update_posts, sender=Form)


class Speakerdeck(Presentation):
    """
    Speakerdeck presentation
    """
    start = models.SmallIntegerField(default=1, verbose_name=_('Start slide'),
        help_text=_('Number of the first slide.'))

    def _regex_id(self):
        try:
            id = re.search('(data-id=")([\d\w.]+)(")', self.embed).group(2)
            return id
        except AttributeError:
#            raise goscale_models.WrongAttribute(attribute='embed')
            return None

    def _get_embed_code(self):
        id = self._regex_id()
        if not id:
            return self.embed
        width, height = self._get_size(extra_height=61)
        return '<iframe class="speakerdeck-iframe goscale-presentation" style="width: %spx; height: %spx; \
            border-top-left-radius: 5px; \
            border-top-right-radius: 5px; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px; \
            border: 0px; background-color: transparent; margin: 0px; padding: 0px; \
            background-position: initial initial; background-repeat: initial initial; " frameborder="0" \
            src="//speakerdeck.com/player/%s?slide=%s" \
            allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>' %  (
                width,
                height,
                id,
                self.start,
            )


class Slideshare(Presentation):
    """
    Slideshare presentation
    """
    start = models.SmallIntegerField(default=1, verbose_name=_('Start slide'),
        help_text=_('Number of the first slide.'))
    without_related_content = models.BooleanField(default=True, verbose_name=_('Without related content'),
        help_text=_('If set related slideshows will not be displayed.'))

    def _regex_id(self):
        try:
            id = re.search('(\/embed_code\/)([\d\w.]+)(\?)', self.embed).group(2)
            return id
        except AttributeError:
            return None
#            raise goscale_models.WrongAttribute(attribute='embed')

    def _get_embed_code(self):
        id = self._regex_id()
        if not id:
            return self.embed
        width, height = self._get_size(default_width=599, extra_height=38)
        return '<iframe src="http://www.slideshare.net/slideshow/embed_code/%s?rel=%s&startSlide=%s" width="%s" \
        height="%s" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="\
        border:1px solid #CCC;border-width:1px 1px 0;margin-bottom:5px" allowfullscreen webkitallowfullscreen \
        mozallowfullscreen> </iframe>' %  (
                id,
                0 if self.without_related_content else 1,
                self.start,
                width,
                height,
            )


DELAY_CHOISES = (
    (1000, _('every second')),
    (2000, _('every 2 seconds')),
    (3000, _('every 3 seconds (default)')),
    (5000, _('every 5 seconds')),
    (10000, _('every 10 seconds')),
    (15000, _('every 15 seconds')),
    (30000, _('every 30 seconds')),
    (60000, _('every minute')),
)

class GooglePresentation(Presentation):
    """
    Google presentation
    """
    delay = models.SmallIntegerField(default=DELAY_CHOISES[2][0], choices=DELAY_CHOISES,
        verbose_name=_('Delay between slides'),
        help_text=_('Automatically advance presentation to the next slide after set delay.'))
    autoplay = models.BooleanField(default=False, verbose_name=_('Autoplay'),
        help_text=_('If set presentation will start automatically.'))
    loop = models.BooleanField(default=False, verbose_name=_('Loop'),
        help_text=_('If set presentation will restart after the last slide.'))

    def _regex_id(self):
        try:
            id = re.search('(\/d\/)([\d\w.]+)(\/embed)', self.embed).group(2)
            return id
        except AttributeError:
            return None
#            raise goscale_models.WrongAttribute(attribute='embed')

    def _get_embed_code(self):
        id = self._regex_id()
        if not id:
            return self.embed
        width, height = self._get_size(extra_height=29)
        return '<iframe src="https://docs.google.com/presentation/d/%s/embed?start=%s&loop=%s&delayms=%s" \
            frameborder="0" width="%s" height="%s" allowfullscreen="true" \
            mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>' %  (
                id,
                'true' if self.autoplay else 'false',
                'true' if self.loop else 'false',
                self.delay,
                width,
                height,
            )