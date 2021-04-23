from django.test import TestCase, Client
import pytest
from django.urls import reverse
from  rest_framework import status
from .models import Bot
from mainapp.api.serializers import BotSerializer

client = Client()

@pytest.mark.django_db
class TestGetFirstBots(TestCase):
    def setUp(self) -> None:
        Bot.objects.create(
            name='Casper', description='Good bot', link='https://web.telegram.org/#/im?p=@casper_bot', author='Nobody')
        Bot.objects.create(
            name='Muffin', description='Very good bot', link='https://web.telegram.org/#/im?p=@muffin_bot', author='Nobody')
        Bot.objects.create(
            name='Rambo', description='Bad bot', link='https://web.telegram.org/#/im?p=@rambo_bot', author='Nobody')
        Bot.objects.create(
            name='Ricky', description='Terrible bot', link='https://web.telegram.org/#/im?p=@ricky_bot', author='Nobody')

    def test_get_all_bots(self):
        response = client.get(reverse('bots'))
        bots = Bot.objects.all()
        serializer = BotSerializer(bots, many=True)
        assert response.data == serializer.data
        assert response.status_code == status.HTTP_200_OK
