from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from projects.management.commands._test_data import load_test_data


class Command(BaseCommand):
    help = 'Flushed the database and fills it with test data'

    def handle(self, *args, **options):
        call_command('flush')
        load_test_data(self.stdout)
