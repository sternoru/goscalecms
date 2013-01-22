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


class Form(goscale_models.GoscaleCMSPlugin):
    """
    Google Form
    """
    url = models.URLField(max_length=250, verbose_name=_('Google Form URL'),
        help_text='ex: https://docs.google.com/spreadsheet/viewform?formkey=cDZ5QkRvZDg5d2Z1Y0l0anEyUVNuZEE6MA')

    def _regex_id(self):
        try:
            return self.url.split('key=')[1]
        except:
            raise goscale_models.WrongAttribute(attribute='url')

    def _get_entry_link(self, entry):
        return 'https://docs.google.com/spreadsheet/formResponse?formkey=%s' % self._regex_id()

    def _get_data(self):
        if not self.url:
            return []
        res = urllib2.urlopen(self.url)
        #TBD get hash and compare to cache value
        return [res.read()]

    def _store_post(self, stored_entry, entry):
        # parse form html
        soup = BeautifulSoup(entry)
        form = soup.find('form')
        description = form.renderContents()
#        print description
        # fill in the fields
        stored_entry.content_type = 'text/html'
        stored_entry.link = self._get_entry_link(entry)
        stored_entry.title = 'Form %d' % self.id
        stored_entry.description = description
        return super(Form, self)._store_post(stored_entry)

#signals.post_save.connect(goscale_models.update_posts, sender=Form)
