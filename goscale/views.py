import urllib2
import urllib

from django import http
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response
from django.template import RequestContext

try:
    from allauth.account.views import signup as allauth_signup
    from allauth.account.forms import LoginForm
    from allauth.account.utils import get_default_redirect
    ALLAUTH = True
except ImportError:
    ALLAUTH = False


def form(request):
    """ Ajax handler for Google Form submition
    """
    if request.method == 'POST':
        url = request.POST['url']
        submit_url = '%s%shl=%s' % (
            url,
            '&' if '?' in url else '?',
            request.LANGUAGE_CODE
        )
        params = urllib.urlencode(request.POST)
        f = urllib2.urlopen(submit_url, params)
        text = f.read()
    else:
        text = _('Error: request type has to be POST')

    response = http.HttpResponse(text, mimetype="text/plain")
    return response


def signup(request, **kwargs):
    """
    Overrides allauth.account.views.signup
    """
    if not ALLAUTH:
        return http.HttpResponse(_('allauth not installed...'))
    if request.method == "POST" and 'login' in request.POST:
        form_class = LoginForm
        form = form_class(request.POST)
        redirect_field_name = "next"
        success_url = get_default_redirect(request, redirect_field_name)
        if form.is_valid():
            return form.login(request, redirect_url=success_url)
    response = allauth_signup(request, **kwargs)
    return response
