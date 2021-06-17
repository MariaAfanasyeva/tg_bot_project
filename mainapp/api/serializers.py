import os

import ldclient
import requests
from django.contrib.auth.models import User
from dotenv import find_dotenv, load_dotenv
from ldclient.config import Config
from rest_framework import serializers

from ..models import Bot, Category, Comment, Like

load_dotenv(find_dotenv(".env.dev"))


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
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

    def validate_link(
        self,
        value,
    ):
        ldclient.set_config(Config(os.environ.get("LD_API_KEY")))

        user = {
            "key": "1111",
        }

        show_feature = ldclient.get().variation("link-validation", user, False)
        if show_feature:
            response = requests.get(value)
            if response.status_code != 200:
                raise serializers.ValidationError("Invalid link")
            return value
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
