GoScale CMS
===========

`GoScale CMS <http://goscalecms.com>`_ is an extension of `Django CMS <http://django-cms.org>`_.

It's a set of unique plugins and useful tools for Django CMS that makes it very powerful by seamlessly integrating content from 3rd party websites like:

* Blogger and Tumblr
* Youtube and Vimeo
* Picasa and Google+
* Google Calendar and Forms
* Any RSS/Atom feeds

But it's more than just content. GoScale plugins add some fancy functionality to make this content shine!

It's perfect for quickly building Mashups and Media heavy sites.

Website: http://goscalecms.com

GitHub repository: https://github.com/sternoru/goscalecms

Documentation
-------------

Please, read our `documentation <https://goscalecms.readthedocs.org>`_ for  the details on installing and using GoScale CMS and it's plugins.

Getting help
------------

Feel free to file issues on github or write to our `mailing list <https://groups.google.com/forum/?fromgroups#!forum/goscale-cms>`_.

Credits
-------

* This is a set of tools and plugins for `Django CMS <http://django-cms.org>`_
* Product of `Sterno.Ru <http://sterno.ru/en/>`_.
* Developed and maintained under supervision of `Evgeny Demchenko <https://github.com/littlepea>`_

Developed with
^^^^^^^^^^^^^^

.. image:: goscale/static/goscale/img/pycharm_logo142x29.gif

Quick start
-----------

We're assuming you're already running a functional version of Django CMS. If not, follow their `tutorial <http://docs.django-cms.org/en/2.2/getting_started/tutorial.html>`_ first:

Install "goscalecms" using pip or easy_install::

    pip install goscalecms

Add "goscale" and desired plugins to your INSTALLED_APPS in settings.py like this::

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


Add GoScale URL patterns to urls.py::

    urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^goscale/', include('goscale.urls')),
        url(r'^', include('cms.urls')),
    )

Sync your Database::

    python manage.py syncdb
    python manage.py migrate

Good to go!

Now if you run you Django server you should have GoScale plugins available for your CMS placeholders.