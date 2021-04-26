from django.test import TestCase, Client
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Bot
from mainapp.api.serializers import BotSerializer
from model_bakery import baker
import json

# client = Client()
#
# @pytest.mark.django_db
# class TestGetFirstBots(TestCase):
#     def setUp(self) -> None:
#         Bot.objects.create(
#             name='Casper', description='Good bot', link='https://web.telegram.org/#/im?p=@casper_bot', author='Nobody')
#         Bot.objects.create(
#             name='Muffin', description='Very good bot', link='https://web.telegram.org/#/im?p=@muffin_bot', author='Nobody')
#         Bot.objects.create(
#             name='Rambo', description='Bad bot', link='https://web.telegram.org/#/im?p=@rambo_bot', author='Nobody')
#         Bot.objects.create(
#             name='Ricky', description='Terrible bot', link='https://web.telegram.org/#/im?p=@ricky_bot', author='Nobody')
#
#     def test_get_all_bots(self):
#         response = client.get(reverse('bots'))
#         bots = Bot.objects.all()
#         serializer = BotSerializer(bots, many=True)
#         assert response.data == serializer.data
#         assert response.status_code == status.HTTP_200_OK

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient


class TestBotsEndpoints:

    def test_list(self, api_client):
        endpoint = reverse('bots')
        baker.make(Bot, _quantity=3)

        response = api_client().get(
            endpoint
        )
        print(json.loads(response.content))

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    # def test_create(self, api_client):
    #     endpoint = reverse('create')
    #     bot = baker.prepare(Bot)
    #     expected_json = {
    #         'name': bot.name,
    #         'description': bot.description,
    #         'link': bot.link,
    #         'author': bot.author,
    #         'id': bot.pk,
    #     }
    #
    #     response = api_client().post(
    #         endpoint,
    #         data=expected_json,
    #         format='json'
    #     )
    #
    #     assert response.status_code == 200
    #     assert json.loads(response.content) == expected_json
    def test_delete(self, api_client):
        bot = baker.make(Bot)
        url = reverse('delete', kwargs={'pk': bot.pk})

        response = api_client().delete(url)

        assert response.status_code == 200
        assert Bot.objects.all().count() == 0

    # def test_update(self, api_client):
    #     old_bot = baker.make(Bot)
    #     new_bot = baker.prepare(Bot)
    #     bot_dict = {
    #         'link': new_bot.link,
    #         'name': new_bot.name,
    #         'description': new_bot.description,
    #         'author': new_bot.author,
    #     }
    #
    #     url = reverse('update', kwargs={'pk': old_bot.pk})
    #
    #     response = api_client().put(
    #         url,
    #         bot_dict,
    #         format='json'
    #     )
    #
    #     assert response.status_code == 200
    #     assert json.loads(response.content) == bot_dict
