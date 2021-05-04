from io import StringIO
from django.core.management import call_command
from django.test import TestCase


class CreateBotTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command('create_bot', stdout=out)
        self.assertIn('Expected outbup', out.getvalue())
