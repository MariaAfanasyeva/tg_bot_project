import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Bot
from model_bakery import baker
import json

pytestmark = pytest.mark.django_db


class TestBotsEndpoints(APITestCase):

    def test_get_list(self):
        endpoint = reverse('bots')
        baker.make(Bot, _quantity=3)
        response = self.client.get(
            endpoint
        )
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_get_one_bot(self):
        bot = baker.make(Bot)

        expected_data = {
            'name': bot.name,
            'description': bot.description,
            'link': bot.link,
            'author': bot.author,
            'id': bot.id,
        }

        endpoint = reverse('detail', kwargs={'pk': bot.id})
        response = self.client.get(endpoint)

        assert response.data == expected_data

    def test_create(self):
        endpoint = reverse('create')
        expected_json = {
            'name': 'My Bot',
            'description': 'Adorable bot',
            'link': 'https//my_bot',
            'author': 'Nobody',
            'id': 1
        }

        response = self.client.post(endpoint, expected_json, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_json

    def test_delete(self):
        bot = baker.make(Bot)
        url = reverse('delete', kwargs={'pk': bot.pk})

        response = self.client.delete(url)

        assert response.status_code == 200
        assert Bot.objects.all().count() == 0

    def test_update(self):
        old_bot = baker.make(Bot)
        new_bot = baker.prepare(Bot)
        bot_dict = {
            'link': new_bot.link,
            'name': new_bot.name,
            'description': new_bot.description,
            'author': new_bot.author,
            'id': old_bot.id,
        }

        url = reverse('update', kwargs={'pk': old_bot.id})

        response = self.client.post(
            url,
            bot_dict,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data == bot_dict
