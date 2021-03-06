from django.core.management.base import BaseCommand
from django.core import management
from django.conf import settings
from goscale.themes import models, site_middleware, set_themes
from cms.models import Page
from django.core.serializers import json, python


class Load(BaseCommand):
    help = "Restores DB and pages separately for each site."

    def handle(self, *args, **options):
        # restore sites and themes if enabled
        file = '%s/fixtures/%s.json' % (settings.PROJECT_PATH, 'sites')
        management.call_command('loaddata', file)
        print 'Restored %s' % file

        if 'goscale.themes' in settings.INSTALLED_APPS:
            file = '%s/fixtures/%s.json' % (settings.PROJECT_PATH, 'themes')
            management.call_command('loaddata', file)
            print 'Restored %s' % file

        # restore users
        file = '%s/fixtures/%s.json' % (settings.PROJECT_PATH, 'auth')
        management.call_command('loaddata', file)
        print 'Restored %s' % file

        # restore placeholders
        file = '%s/fixtures/%s.json' % (settings.PROJECT_PATH, 'placeholders')
        management.call_command('loaddata', file)
        print 'Restored %s' % file
#
#        # restore pages
        try:
            for theme in models.Theme.objects.all():
                site = theme.sites.all()[0]
                # set theme
                site_middleware.SITE_ID.value = site.id
                set_themes()
                # load pages
                file = '%s/fixtures/pages_%s.json' % (settings.PROJECT_PATH, theme.name)
                management.call_command('loaddata', file)
                print 'Restored %s' % file
        except Exception, e:
            print 'Couldn\'t load themes: %s' % str(e)
            file = '%s/fixtures/pages.json' % settings.PROJECT_PATH
            management.call_command('loaddata', file)
            print 'Restored %s' % file

        # restore the cms
        file = '%s/fixtures/%s.json' % (settings.PROJECT_PATH, 'cms')
        management.call_command('loaddata', file)
        print 'Restored %s' % file

        if not options['cms_only']:
            # restore the rest
            file = '%s/fixtures/%s.json' % (settings.PROJECT_PATH, 'rest')
            management.call_command('loaddata', file)
            print 'Restored %s' % file