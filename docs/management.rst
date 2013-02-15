3. Management commands
====================

3.1. update_slugs
---------------------

Re-saves all posts for all GoScale plugins and re-generates slugs based on post titles and IDs.

Usage::

    python manage.py update_slugs

3.1. update_posts
---------------------

Updates posts for all GoScale plugins.

You can put run it manually or as a cron job to keep your plugins content up-to-date and cached. But the best way to do it is by using Celery task queue!

Usage::

    python manage.py update_posts