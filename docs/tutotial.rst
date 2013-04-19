1. Quick Start Tutorial
=======================

1.1. Installation
------------------

Install using pip or easy_install::

    pip install goscalecms

settings.py
^^^^^^^^^^^^^^^^^^

Add "goscale" and desired plugins to your INSTALLED_APPS setting like this (also add "cms" and django-cms plugins if you haven't yet::

      INSTALLED_APPS = (
          ...
          # django-cms related apps:
          'cms',
          'mptt',
          'menus',
          'sekizai',
          'cms.plugins.text',
          'cms.plugins.snippet',
          'cms.plugins.file',
          'cms.plugins.image',
          'cms.plugins.teaser',
          'cms.plugins.video',

          # goscalecms related apps:
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

Add GoScale and django-cms URL patterns::

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