from django.conf import settings
from django.core.cache import cache
from django.contrib.sites.models import Site
from . import set_themes


def make_tls_property(default=None):
    """Creates a class-wide instance property with a thread-specific value."""
    class TLSProperty(object):
        def __init__(self):
            from threading import local
            self.local = local()

        def __get__(self, instance, cls):
            if not instance:
                return self
            return self.value

        def __set__(self, instance, value):
            self.value = value

        def _get_value(self):
            return getattr(self.local, 'value', default)
        def _set_value(self, value):
            self.local.value = value
        value = property(_get_value, _set_value)

    return TLSProperty()

SITE_ID = settings.__dict__['_wrapped'].__class__.SITE_ID = make_tls_property(settings.SITE_ID)
THEME = settings.__dict__['_wrapped'].__class__.THEME = make_tls_property(settings.THEME)

class SiteOnFlyDetectionMiddleware:
    def process_request(self, request):
        self.request = request
        self.site = None
        self.SITE_ALIASES = getattr(settings, "SITE_ALIASES", None)
        self.theme = None
        self.domain, self.port = self.get_domain_and_port()
        self.domain_requested = self.domain
        self.domain_unsplit = self.domain
        self.subdomain = None
        self.env_domain_requested = None

        # main loop - lookup the site by domain/subdomain, plucking
        # subdomains off the request hostname until a site or
        # redirect is found
        res = self.lookup()
#        res = self.theme_lookup()

        set_themes()

    def get_domain_and_port(self):
        """
        Django's request.get_host() returns the requested host and possibly the
        port number.  Return a tuple of domain, port number.
        Domain will be lowercased
        """
        host = self.request.get_host()
        if ':' in host:
            domain, port = host.split(':')
        else:
            domain = host
            port = self.request.META.get('SERVER_PORT')
        if self.SITE_ALIASES and domain in self.SITE_ALIASES:
            domain = self.SITE_ALIASES[domain]
        return (domain.lower(), port)

    def lookup(self):
        """
        The meat of this middleware.

        Returns None and sets settings.SITE_ID if able to find a Site
        object by domain and its subdomain is valid.

        Returns an HttpResponsePermanentRedirect to the Site's default
        subdomain if a site is found but the requested subdomain
        is not supported, or if domain_unsplit is defined in
        settings.HOSTNAME_REDIRECTS

        Otherwise, returns False.
        """

        # check to see if this hostname is actually a env hostname
        if self.domain:
            if self.subdomain:
                self.domain_unsplit = '%s.%s' % (self.subdomain, self.domain)
            else:
                self.domain_unsplit = self.domain
            self.domain_requested = self.domain_unsplit

        # check cache
        cache_key = 'site_id:%s' % self.domain_unsplit
        site_id = cache.get(cache_key)
        if site_id:
            SITE_ID.value = site_id
            try:
                self.site = Site.objects.get(id=site_id)
            except Site.DoesNotExist:
                # This might happen if the Site object was deleted from the
                # database after it was cached.  Remove from cache and act
                # as if the cache lookup failed.
                cache.delete(cache_key)
            else:
                return None

        # check database
        try:
            self.site = Site.objects.get(domain=self.domain)
        except Site.DoesNotExist:
            return False
        if not self.site:
            return False

        SITE_ID.value = self.site.pk
        cache.set(cache_key, SITE_ID.value, 5*60)
        return None

    def theme_lookup(self):
        """
        Returns theme based on site

        Returns None and sets settings.THEME if able to find a theme object by site.

        Otherwise, returns False.
        """

        # check cache
        cache_key = 'theme:%s' % self.domain_unsplit
        theme = cache.get(cache_key)
        if theme:
            THEME.value = theme
            return None

        # check database
        if hasattr(self.site, 'theme_set'):
            try:
                themes = [theme.name for theme in self.site.theme_set.all()]
                THEME.value = themes[0]
                cache.set(cache_key, THEME.value, 5*60)
            except:
                return False
        return None
