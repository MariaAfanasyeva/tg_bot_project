import os

import ldclient
import requests
from django.contrib.auth.models import User
from dotenv import find_dotenv, load_dotenv
from ldclient.config import Config
from rest_framework import serializers

from ..models import Bot, BotCollection, Category, Comment, Like

load_dotenv(find_dotenv(".env.dev"))


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CollectionSerializer(serializers.ModelSerializer):
    bot = serializers.PrimaryKeyRelatedField(queryset=Bot.objects.all(), many=True)

    class Meta:
        model = BotCollection
        fields = "__all__"


class BotSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="name",
        read_only=False,
        queryset=Category.objects.all(),
        allow_null=True,
        allow_empty=True,
        required=False,
    )

    @staticmethod
    def check_link(link):
        obj_with_link = Bot.objects.filter(link__iexact=link)
        if obj_with_link:
            raise serializers.ValidationError(
                "Bot with the same link is already in database"
            )
        else:
            return link

    def validate_link(
        self,
        value,
    ):
        ldclient.set_config(Config(os.environ.get("LD_API_KEY")))

        user = {
            "key": "1111",
        }

        show_feature = ldclient.get().variation("link-validation", user, False)
        method = self.context["request"].method
        if method != "PUT":
            value = self.check_link(value)
        if show_feature:
            response = requests.get(value)
            if response.status_code != 200:
                raise serializers.ValidationError("Invalid link")
        return value
        ldclient.close()

    class Meta:
        model = Bot
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    to_bot = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    to_bot = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Like
        fields = "__all__"
