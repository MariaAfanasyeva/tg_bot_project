from model_bakery import baker
from mainapp.models import Bot
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create random bots'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--total', type=int, default=1, help='Indicates the number of bots to be created')

    def handle(self, *args, **options):
        total = options['total']
        for _ in range(total):
            bot = baker.prepare(Bot)
            bot.save()
            self.stdout.write(self.style.SUCCESS('Successfully created bot'))
