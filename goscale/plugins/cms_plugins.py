from cms.plugin_base import CMSPluginBase

class GoscaleCMSPluginBase(CMSPluginBase):
    """
    Base class for GoScale plugins
    """
    exclude = ('posts',)

    def render(self, context, instance, placeholder):
        context['posts'] = [post.json() for post in instance.posts.all()]
        return context