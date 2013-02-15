from django.core.management.base import BaseCommand
from django.utils.timesince import timesince
from django.utils.encoding import smart_str

class Command(BaseCommand):
    help = "Update posts for all plugins."

    def handle(self, *args, **options):
        from goscale import utils
        for plugin in utils.get_plugins():
            print 'Updating GoScale plugin: %s (%s)' % (plugin, plugin.id)
            instance, count = utils.update_plugin(plugin.id)
            print 'Updated %d posts for %s (%d)' % (count, plugin, plugin.id)
