from django.core.management.base import BaseCommand


class UpdateSlugs(BaseCommand):
    help = "Update slugs for all posts."

    def handle(self, *args, **options):
        from goscale.models import Post
        # Re-save all posts
        print 'Re-saving all posts...'
        print
        for post in Post.objects.all():
            post.save()
            print 'Post slug: %s' % post.slug
        print
        print 'Slugs updated.'