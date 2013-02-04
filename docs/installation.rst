1. Getting started
==================

1.1. Requirements
------------------

Required
^^^^^^^^^^^^^^^^^^

* django-cms 2.2 or higher
* pytz
* unidecode
* BeautifulSoup
* feedparser
* gdata

Recommended
^^^^^^^^^^^^^^^^^^

* django-filer with its django CMS plugins, file and image management application to use instead of some core plugins
* django-cms-themes

Note:

When installing the GoScale CMS using pip, Django, django-cms, pytz, unidecode, BeautifulSoup, feedparser and gdata will be installed automatically.

1.2. Installation
------------------

We're assuming you're already running a functional version of Django CMS. If not, follow their tutorial_ first:

.. _tutorial: http://docs.django-cms.org/en/2.2/getting_started/tutorial.html

Python package
^^^^^^^^^^^^^^^^^^

Install using pip or easy_install::

    pip install goscalecms

settings.py
^^^^^^^^^^^^^^^^^^

Add "goscale" and desired plugins to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'goscale',
          'goscale.plugins.videos',
          'goscale.plugins.pictures',
          'goscale.plugins.feeds',
          'goscale.plugins.forms',
          'goscale.plugins.calendar',
          'goscale.plugins.presentations',
      )

urls.py
^^^^^^^^^^^^^^^^^^

Add GoScale URL patterns::

      urlpatterns = patterns('',
          url(r'^admin/', include(admin.site.urls)),
          url(r'^goscale/', include('goscale.urls')),
          url(r'^', include('cms.urls')),
      )

Sync your Database
^^^^^^^^^^^^^^^^^^

Run::

    python manage.py syncdb
    python manage.py migrate

Good to go!
^^^^^^^^^^^^^^^^^^

Now if you run you Django server you should have GoScale plugins available for your CMS placeholders.