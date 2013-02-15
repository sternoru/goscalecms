4. Celery tasks
====================

The best way to keep your content up-to-date is by running a Celery worker that will update and cache all the plugins.

It's easy to get it up and running.

1. Install the django-celery library::

    pip install django-celery

2. Add the following lines to settings.py::

    import djcelery
    djcelery.setup_loader()

3. Add 'djcelery' to INSTALLED_APPS.

4. syncdb or migrate if you're using south::

    python manage.py migrate djcelery

5. Configure your tasks in settings.py::

    BROKER_URL = 'amqp://guest:guest@localhost:5672/' # if you're using RabbitMQ
    CELERY_IMPORTS = ("goscale.tasks", )

6. If you want a task to update GoScale plugins to be sent immediately after plugin was saved in the Django admin add this in your settings::

    GOSCALE_UPDATE_FROM_ADMIN = True

7. If you want to setup a schedule for updating, configure Celery Beat::

    from celery.schedules import crontab

    CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler' # or whatever you prefer

    CELERYBEAT_SCHEDULE = {
        "update_goscale_plugins": {
            "task": "goscale.tasks.update_goscale_plugins",
            "schedule": crontab(minute='*/30'), # every 30 minutes
            "args": ()
        },
    }

8. Run your worker and celery beat::

    python manage.py celery worker -B

For more detailed information refer to `Celery documentation`_.

.. _Celery documentation: http://docs.celeryproject.org/en/latest/django/


4.1. update_goscale_plugins
---------------------

Periodic task that goes through all goscale plugins and sends tasks to update them.

4.2. update_goscale_plugin_posts
---------------------

Updates posts for a single plugin.

Usually scheduled by **update_goscale_plugins** task or when saving a plugin from Django admin.