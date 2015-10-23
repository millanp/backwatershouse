from django.core.management.base import BaseCommand
from backend import helpers
class Command(BaseCommand):
    help = 'tests the google calendar api implementation'
    def handle(self, *args, **options):
        helpers.calendar_test()