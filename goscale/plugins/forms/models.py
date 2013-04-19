import re
import simplejson
import datetime
import urllib2
import BeautifulSoup

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
    form_class = models.CharField(max_length=50, verbose_name=_('Form class'), null=True, blank=True,
        help_text=_('Additional class attribute to add to the form element.'))

    def copy_relations(self, oldinstance):
        # FIXME: remove after this issue is resolved: https://github.com/divio/django-cms/issues/1723
        super(Form, self).copy_relations(oldinstance)

    def _regex_id(self):
        try:
            if 'key=' in self.url:
                pattern = '(key=)([\d\w-]+)(#)?'
                form_url = 'https://docs.google.com/spreadsheet/formResponse?formkey=%s'
            else:
                pattern = '(\/d\/)([\d\w-]+)(\/)?'
                form_url = 'https://docs.google.com/forms/d/%s/formResponse'
            key = re.search(pattern, self.url).group(2)
            return key, form_url
        except AttributeError:
            raise goscale_models.WrongAttribute(attribute='url')

    def _get_entry_link(self, entry=None):
        key, form_url = self._regex_id()
        return form_url % key

    def _get_data(self):
        if not self.url:
            return []
        res = urllib2.urlopen(self.url)
        #TBD get hash and compare to cache value
        return [res.read()]

    def _store_post(self, stored_entry, entry):
        # parse form html
#        try:
#            soup = BeautifulSoup.ICantBelieveItsBeautifulSoup(entry)
#        except (TypeError, AttributeError):
#            soup = BeautifulSoup.BeautifulSoup.ICantBelieveItsBeautifulSoup(entry)
#        form = soup.find('form')
#        print entry
#        print form
#        description = form.renderContents()
        description = entry[entry.find('<form'):entry.find('</form')+7].replace(
            'Never submit passwords through Google Forms.',
            ''
        )
        if self.form_class: # apply a custom class to a form
            description = description.replace(
                'ss-form',
                'ss-form %s' % self.form_class
            )
        # fill in the fields
        stored_entry.content_type = 'text/html'
        stored_entry.link = self._get_entry_link(entry)
        stored_entry.title = 'Form %d' % self.id
        stored_entry.description = description
        return super(Form, self)._store_post(stored_entry)

#signals.post_save.connect(goscale_models.update_posts, sender=Form)
