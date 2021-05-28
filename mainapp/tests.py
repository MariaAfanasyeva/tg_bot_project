import json
from io import StringIO
from optparse import make_option

import jwt
import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from dotenv import dotenv_values
from model_bakery import baker
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient, APITestCase
from rest_framework_jwt.settings import api_settings

from .models import Bot

pytestmark = pytest.mark.django_db
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class TestBotsEndpoints(APITestCase):
    def setUp(self) -> None:
        self.username = "usuario"
        self.password = "contrasegna"
        self.credentials = {"username": self.username, "password": self.password}
        self.jwt_url = "http://127.0.0.1:8000/api/token/"

    def test_get_list(self):
        endpoint = reverse("bots")
        baker.make(Bot, _quantity=4)
        response = self.client.get(endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4

    def test_get_one_bot(self):
        bot = baker.make(Bot)

        expected_data = {
            "name": bot.name,
            "description": bot.description,
            "link": bot.link,
            "author": bot.author,
            "id": bot.id,
            "category": None,
            "add_by_user": None,
        }

        endpoint = reverse("detail", kwargs={"pk": bot.id})
        response = self.client.get(endpoint)

        assert response.data == expected_data

    def test_create_user_not_authenticated(self):
        endpoint = reverse("create")
        expected_json = {
            "detail": ErrorDetail(
                string="Authentication credentials were not provided.",
                code="not_authenticated",
            )
        }

        response = self.client.post(endpoint, expected_json, format="json")
        assert response.status_code == 401
        assert response.data == expected_json

    def test_create_user_authenticated(self):
        user = User.objects.create_user(
            username=self.username,
            email="usuario@mail.com",
            password=self.password,
            id=1,
        )
        response = self.client.post(self.jwt_url, self.credentials, format="json")
        access_key = response.data["access"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_key)
        endpoint = reverse("create")
        data_json = {
            "name": "My Bot",
            "description": "Adorable bot",
            "link": "https://my_bot",
            "author": "Nobody",
        }
        expected_json = {
            "name": "My Bot",
            "description": "Adorable bot",
            "link": "https://my_bot",
            "author": "Nobody",
            "category": None,
            "add_by_user": user.id,
            "id": 1,
        }

        response = client.post(endpoint, data_json, format="json")
        assert response.status_code == 201
        assert response.data == expected_json

    def test_delete_by_owner(self):
        user = User.objects.create_user(
            username=self.username,
            email="usuario@mail.com",
            password=self.password,
            id=1,
        )
        bot = Bot.objects.create(
            name="AAAA", description="BBB", link="CCC", author="DDDD", add_by_user=user
        )
        response = self.client.post(self.jwt_url, self.credentials, format="json")
        access_key = response.data["access"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_key)
        url = reverse("delete", kwargs={"pk": bot.pk})

        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Bot.objects.all().count() == 0

    def test_delete_by_other_user(self):
        user1 = User.objects.create_user(
            username=self.username,
            email="usuario@mail.com",
            password=self.password,
            id=1,
        )
        user2 = User.objects.create_user(
            username="aaa",
            email="usuario@mail.com",
            password="aaa",
            id=2,
        )
        bot = Bot.objects.create(
            name="AAAA", description="BBB", link="CCC", author="DDDD", add_by_user=user2
        )
        response = self.client.post(self.jwt_url, self.credentials, format="json")
        access_key = response.data["access"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_key)
        url = reverse("delete", kwargs={"pk": bot.pk})

        response = client.delete(url)

        assert response.status_code == 403
        assert Bot.objects.all().count() == 1

    def test_update_by_owner(self):
        user = User.objects.create_user(
            username=self.username,
            email="usuario@mail.com",
            password=self.password,
            id=1,
        )
        bot1 = Bot.objects.create(
            name="AAAA", description="BBB", link="CCC", author="DDDD", add_by_user=user
        )
        bot_dict = {
            "link": "ccc",
            "name": "aaaa",
            "description": "bbbb",
            "author": "dddd",
            "id": bot1.id,
            "category": None,
            "add_by_user": user.id,
        }
        response = self.client.post(self.jwt_url, self.credentials, format="json")
        access_key = response.data["access"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_key)
        url = reverse("update", kwargs={"pk": bot1.id})

        response = client.put(url, bot_dict, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == bot_dict

    def test_update_by_other_user(self):
        user1 = User.objects.create_user(
            username=self.username,
            email="usuario@mail.com",
            password=self.password,
            id=1,
        )
        user2 = User.objects.create_user(
            username="aaa",
            email="usuario@mail.com",
            password="aaa",
            id=2,
        )
        bot1 = Bot.objects.create(
            name="AAAA", description="BBB", link="CCC", author="DDDD", add_by_user=user2
        )
        bot_dict = {
            "link": "ccc",
            "name": "aaaa",
            "description": "bbbb",
            "author": "dddd",
            "id": bot1.id,
            "category": None,
            "add_by_user": user2.id,
        }
        response = self.client.post(self.jwt_url, self.credentials, format="json")
        access_key = response.data["access"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_key)
        url = reverse("update", kwargs={"pk": bot1.id})

        response = client.put(url, bot_dict, format="json")

        assert response.status_code == 403


class CreateBotTest(TestCase):
    def test_create_bot(self):
        out = StringIO()
        make_option("--total", dest="total", type=int, help="Help description...")
        call_command("create_bot", total=2, stdout=out)
        print(out)


class LoginTest(APITestCase):
    def setUp(self) -> None:
        self.username = "usuario"
        self.password = "contrasegna"
        self.credentials = {"username": self.username, "password": self.password}
        self.jwt_url = "http://127.0.0.1:8000/api/token/"

    def test_incorrect_credentials(self):
        self.credentials = {"username": self.username, "password": "wrongPassword"}
        response = self.client.post(self.jwt_url, self.credentials)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_correct_credentials(self):
        user = User.objects.create_user(
            username=self.username, email="usuario@mail.com", password=self.password
        )
        response = self.client.post(self.jwt_url, self.credentials, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_token_is_returned(self):
        user = User.objects.create_user(
            username=self.username, email="usuario@mail.com", password=self.password
        )
        response = self.client.post(self.jwt_url, self.credentials, format="json")
        assert isinstance(response.data["access"], str)
        assert isinstance(response.data["refresh"], str)

    def test_is_right_format(self):
        user = User.objects.create_user(
            username=self.username, email="usuario@mail.com", password=self.password
        )
        response = self.client.post(self.jwt_url, self.credentials, format="json")
        access_key = response.data["access"]
        secret_key = dotenv_values(".env.dev")["SECRET_KEY"]
        decoded = jwt.decode(access_key, secret_key, algorithms="HS256")
        assert decoded["token_type"] == "access"
