from django.core.management.base import BaseCommand
from django.core import management
from django.core import serializers
from django.conf import settings
from goscale.themes import models, site_middleware
from cms.models import Page
from filer.models import Image, File, Folder
from goscale.models import Post


class Dump(BaseCommand):
    help = "Dumps DB and pages separately for each site."

    def handle(self, *args, **options):
        dump_format = 'json' #'json-pretty'
        # delete posts
        Post.objects.all().delete()

        # serialize pages
        try:
            for theme in models.Theme.objects.all():
                site = theme.sites.all()[0]
                pages = Page.objects.filter(site=site)
                file = '%s/fixtures/pages_%s.json' % (settings.PROJECT_PATH, theme.name)
                with open(file, 'w+') as f:
                    f.write(serializers.serialize(dump_format, pages, indent=4, use_natural_keys=True))
                print 'Saved %s' % file
        except Exception, e:
            print 'Couldn\'t load themes: %s' % str(e)
            pages = Page.objects.all()
            file = '%s/fixtures/pages.json' % settings.PROJECT_PATH
            with open(file, 'w+') as f:
                f.write(serializers.serialize(dump_format, pages, indent=4, use_natural_keys=True))
            print 'Saved %s' % file

        # serialize themes if enabled
        if 'goscale.themes' in settings.INSTALLED_APPS:
            file = '%s/fixtures/%s.json' % (settings.PROJECT_PATH, 'themes')
            with open(file, 'w+') as f:
                management.call_command('dumpdata', 'themes', indent=4, use_natural_keys=True, stdout=f, format=dump_format)
            print 'Saved %s' % file

        # serialize the rest
        file = '%s/fixtures/%s.json' % (settings.PROJECT_PATH, 'sites')
        with open(file, 'w+') as f:
            management.call_command('dumpdata', 'sites', indent=4, use_natural_keys=True, stdout=f, format=dump_format)
        print 'Saved %s' % file

        file = '%s/fixtures/%s.json' % (settings.PROJECT_PATH, 'auth')
        with open(file, 'w+') as f:
            management.call_command('dumpdata', 'auth', indent=4, exclude=['auth.Permission'],
                                    use_natural_keys=True, stdout=f, format=dump_format)
        print 'Saved %s' % file

        file = '%s/fixtures/%s.json' % (settings.PROJECT_PATH, 'placeholders')
        with open(file, 'w+') as f:
            management.call_command('dumpdata', 'cms.Placeholder', indent=4, use_natural_keys=True, stdout=f,
                                    format=dump_format)
        print 'Saved %s' % file

        file = '%s/fixtures/%s.json' % (settings.PROJECT_PATH, 'cms')
        with open(file, 'w+') as f:
            management.call_command('dumpdata', 'cms', indent=4, use_natural_keys=True, use_base_manager=True, exclude=[
                'cms.Placeholder',
                'cms.Page',
                ], stdout=f, format=dump_format)
        print 'Saved %s' % file

        if not options['cms_only']:
            file = '%s/fixtures/%s.json' % (settings.PROJECT_PATH, 'rest')
            with open(file, 'w+') as f:
                management.call_command('dumpdata', indent=4, use_natural_keys=True, use_base_manager=True, exclude=[
                    'contenttypes',
                    'auth',
                    'sessions.Session',
                    'goscale.Post',
                    'cms',
                    'admin',
                    'sites',
                    'themes',
                    ], stdout=f, format=dump_format)
            print 'Saved %s' % file