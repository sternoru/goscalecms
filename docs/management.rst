3. Management commands
====================

3.1. goscale
---------------------

All the commands in GoScale CMS are grouped under one command "goscale". Run it with `--help` option to list all available commands::

    python manage.py goscale --help

3.2. update_slugs
---------------------

Re-saves all posts for all GoScale plugins and re-generates slugs based on post titles and IDs.

Usage::

    python manage.py goscale update_slugs

3.1. update_posts
---------------------

Updates posts for all GoScale plugins.

You can put run it manually or as a cron job to keep your plugins content up-to-date and cached. But the best way to do it is by using Celery task queue!

Available options:

* -s, --site - Site ID to filter plugins.
* -t, --theme - Theme name to filter plugins.

Usage::

    python manage.py goscale update_posts --site=2