from django.core.management.base import BaseCommand

from angleMonitor import publisher_emulator


class Command(BaseCommand):
    help = 'Generates mock data for testing the database performance'

    def handle(self, *args, **kwargs):
        if len(args) == 0:
            data_qty = 500000
        else:
            data_qty = int(args[0])
        publisher_emulator.publish()
