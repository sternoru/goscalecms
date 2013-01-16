import urllib2
import urllib

from django import http
from django.utils.translation import ugettext as _


def form(request):
    """ Ajax handler for Google Form submition
    """
    if request.method == 'POST':
        submit_url = '%s&hl=%s' % (
            request.POST['url'],
            request.LANGUAGE_CODE
        )
        params = urllib.urlencode(request.POST)
        f = urllib2.urlopen(submit_url, params)
        text = f.read()
    else:
        text = _('Error: request type has to be POST')

    response = http.HttpResponse(text, mimetype="text/plain")
    return response
