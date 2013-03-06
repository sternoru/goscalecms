from cms.models import CMSPlugin
from goscale import utils
from celery.task import task
from celery.execute import send_task

@task(name='goscale.tasks.update_goscale_plugins')
def update_goscale_plugins():
    for plugin in utils.get_plugins():
        print 'Sending GoScale plugin for updating: %s (%s)' % (plugin, plugin.id)
        send_task('goscale.tasks.update_goscale_plugin_posts', [plugin.id])

@task(name='goscale.tasks.update_goscale_plugin_posts')
def update_goscale_plugin_posts(plugin_id):
    instance, count = utils.update_plugin(plugin_id)
    if instance:
        print 'Updated %d posts for %s (%d)' % (count, instance, plugin_id)
    else:
        print 'Couldn\'t update posts for plugin_id: %d' % plugin_id
    return instance