1. Template tags
====================

Usage of GoSCale template tags is optional but can provide some useful functionality.

Tag library for GoScale is called "goscale_tags"::

    {% load goscale_tags %}

1.1. Paginator
--------------------

Provides a simple reusable pagination for GoScale plugin posts.

Usage examples
^^^^^^^^^^^^^^^^^^^^

Simple case::

    {% goscale_paginator %}

Custom template::

    {% goscale_paginator template="infinite_scrolling.html" %}

Tag info
^^^^^^^^^^^^^^^^^^^^

Tag: goscale_paginator

Template: paginator.html

Keyword arguments:

* template - if you want to use a custom template instead of paginator.html provide your template file.

Context variables:

* {{ paginator }} - Actual Django paginator instance
* {{ page }} - Current page instance
* {{ page_range }} - Smart list of pages to display

Note: if you want a full unfiltered list of all pages just use {{ paginator.page_range }}

1.2. Plugin filters
--------------------

If your plugin uses any complex filters or query string params for it's data you can use this tag to generate links to pass these filters to your plugin (or even all plugins on a page with the "global" param).

It renders the whole query string with added filters for the current plugin so any other query string params will be preserved. You can ignore this  default behavior  by using "exclusive" param.

One of the examples is in the paginator tag to generate page links and in calendar plugin to generate start date links.

Usage examples
^^^^^^^^^^^^^^^^^^^^

Page link::

    <a href="{% goscale_plugin_filters page=page.previous_page_number %}">{% trans "Prev" %}</a>

Calendar date example::

    <a href="{% goscale_plugin_filters start=start_date global='true' exclusive='true' %}">{{start_date}}</a>

Tag info
^^^^^^^^^^^^^^^^^^^^

Tag: goscale_plugin_filters

Keyword arguments:

* Any number of filters you want to pass (ex: page=, start=, sort=...)
* global - if 'true' these filters will apply to  all the plugins, not just the one you're using the tag from (very useful for sharing filters between plugins like datepicker and events for Calendar)
* exclusive - if 'true' only this filters will be rendered as a query string, any other params will be ignored.

1.3. Plugin post
--------------------

Used to render a link for a single post.

Usage examples
^^^^^^^^^^^^^^^^^^^^

Post link::

    <a href="{% goscale_plugin_post post %}">{{ post.title }}</a>

Tag info
^^^^^^^^^^^^^^^^^^^^

Tag: goscale_plugin_post

Arguments:

* post - Post instance to link to

1.4. GoScale Placeholder
--------------------

Simply an extension of Django CMS placeholder_ tag. It acts exactly the same but allows you to define if you want to render single posts into this placeholder.

.. _placeholder: http://docs.django-cms.org/en/2.3.5/advanced/templatetags.html#placeholder

For example if you  want to render posts from "sidebar" placeholder plugins into "content" placeholder which can often be a case.

If you don't use it you will still be able to access single posts inside of your plugin in a {{ post }} context variable.

Usage examples
^^^^^^^^^^^^^^^^^^^^

Same result as Django CMS placeholder::

    {% goscale_placeholder content %}

Placeholder where to render single posts::

    {% goscale_placeholder content render_posts='true' %}

Tag info
^^^^^^^^^^^^^^^^^^^^

Tag: goscale_placeholder

Keyword arguments:

* render_posts - if 'true' single posts will be rendered into this placeholder overriding any plugins it might have

1.5. GoScale AddtoBlock
--------------------

Simply an extension of django-sekizai addtoblock_ tag. It acts exactly the same but allows you to use it with AJAX requests.

.. _addtoblock: http://django-sekizai.readthedocs.org/en/latest/usage.html#template-tag-reference

If a CMS plugin where you use it will be rendered inside of an AJAX request it will simply render the contents of addtoblock tag instead of adding them into page context which wouldn't work with ajax anyway.

Usage examples
^^^^^^^^^^^^^^^^^^^^

Same result as sekizai addtoblock::

    {% goscale_addtoblock js %}

Tag info
^^^^^^^^^^^^^^^^^^^^

Tag: goscale_addtoblock

Arguments:

* name - name on the block in the base template

1.6. User
--------------------

Renders a user bar for Login and Registration links and User Info.

Usage examples
^^^^^^^^^^^^^^^^^^^^

Simple case::

    {% goscale_user %}

Custom template::

    {% goscale_user template="userbar.html" %}

Tag info
^^^^^^^^^^^^^^^^^^^^

Tag: goscale_user

Template: user/user.html

Keyword arguments:

* template - if you want to use a custom template instead of user.html provide your template file.

1.7. Login
--------------------

Renders a Login Form  to use outside of the /accounts/login/ page.

Usage examples
^^^^^^^^^^^^^^^^^^^^

Simple case::

    {% goscale_login %}

Custom template::

    {% goscale_login template="custom_login.html" %}

Tag info
^^^^^^^^^^^^^^^^^^^^

Tag: goscale_login

Template: user/login.html

Keyword arguments:

* template - if you want to use a custom template instead of login.html provide your template file.