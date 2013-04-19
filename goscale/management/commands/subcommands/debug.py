from django.core.management.base import BaseCommand
from django.conf import settings
from goscale.themes import set_themes


class Debug(BaseCommand):
    help = "Debug command for devs."

    def handle(self, *args, **options):
        set_themes()
        print 'TEMPLATE_DIRS: %s' % settings.TEMPLATE_DIRS
