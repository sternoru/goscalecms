from django.core.management.base import BaseCommand


class UpdatePosts(BaseCommand):
    help = "Updates posts for all plugins."

    def handle(self, *args, **options):
        from goscale import utils
        sites = []
        if options['site']:
            from django.contrib.sites.models import Site
            sites.append(Site.objects.get(pk=int(options['site'])))
        elif options['theme']:
            from goscale.themes.models import Theme
            sites.extend(Theme.objects.get(name=options['theme']).get_sites())
        # print 'SITES:', sites
        # print 'PLUGINS:', utils.get_plugins(sites)
        for plugin in utils.get_plugins(sites):
            print 'Updating GoScale plugin: %s (%s)' % (plugin, plugin.id)
            instance, count = utils.update_plugin(plugin.id)
            print 'Updated %d posts for %s (%d)' % (count, plugin, plugin.id)
