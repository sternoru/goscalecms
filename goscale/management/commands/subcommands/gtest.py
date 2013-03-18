from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = '<command>'
    help = "Debugging for GoScale (DEV)."

    def handle(self, *args, **options):
        print args
        self.test()

    def test(self):
        print 'test'