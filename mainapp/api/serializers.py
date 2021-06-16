from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import Bot, Category, Comment, Like


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
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Like
        fields = "__all__"
