3. Themes support
====================

It's possible to enable different themes for different sites using 'goscale.themes' app.

It's a combination of modified django-cms-themes_ and django-dynamicsites_

.. _django-cms-themes: https://github.com/MegaMark16/django-cms-themes
.. _django-dynamicsites: https://bitbucket.org/uysrc/django-dynamicsites/overview

Currently it's possible to theme:

* CSS/JS/Images (static files)
* Templates
* Theme settings (if theme_settings.py is present)

3.1. Installation
---------------------

To use themes add 'goscale.themes' to INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'goscale',
        'goscale.themes',
    )

Add 'static' context processor::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'goscale.themes.context_processors.static',
    )

Add 'SiteOnFlyDetectionMiddleware' middleware before any other::

    MIDDLEWARE_CLASSES = (
        'goscale.themes.site_middleware.SiteOnFlyDetectionMiddleware',
        ...
    )

3.2. Usage
---------------------

Create a new Theme in django admin and upload a theme tarball (tar.gz) file or put your theme files into 'themes' directory in your project and input the theme name.

Choose a Site to which this theme should apply.

After that you should have theme templates in your Page editing form.

For more information refer to django-cms-themes website_.

.. _website: http://www.djangocmsthemes.com/

3.3. Using theme files in templates
---------------------

For theme static files::

    {{ STATIC_THEME_URL }}

For current theme name::

    {{ GOSCALE_THEME }}

3.4. Theme switching on request
---------------------

The beauty of goscale.themes app is that you can serve multiple themes and sites from the same django project instance. It's enabled by SiteOnFlyDetectionMiddleware from django-dynamicsites.

You can switch themes dynamically by hosts in your browser.

For more information refer to django-dynamicsites documentation_.

.. _documentation: https://bitbucket.org/uysrc/django-dynamicsites/overview

To enable multiple hosts for one theme (for example local, dev, staging servers) use SITE_ALIASES setting::

    SITE_ALIASES = {
        'goscalecms.ru': 'goscalecms.com',
    }

3.5. Debugging theme switching
---------------------

The pattern for theme switching locally is::

    {{theme}}.127.0.0.1.xip.io:{{port}}

So let's say you're running your server on localhost:8000. And you want to open theme goscale, then open::

    http://goscale.127.0.0.1.xip.io:8000/