import ldclient
import requests
from django.contrib.auth.models import User
from ldclient.config import Config
from rest_framework import serializers

from ..models import Bot, Category, Comment


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
    ldclient.set_config(Config("sdk-c213fb71-0a88-44e3-907d-bb83ed45b8a2"))

    ld_client = ldclient.get()
    user = {
        "key": "1111",
    }

    show_feature = ldclient.get().variation("link-validation", user, False)

    if show_feature:

        def validate_link(self, value):
            response = requests.get(value)
            if response.status_code != 200:
                raise serializers.ValidationError("Invalid link")
            return value

    ldclient.get().close()

    class Meta:
        model = Bot
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    to_bot = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
