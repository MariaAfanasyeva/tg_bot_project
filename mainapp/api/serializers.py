from rest_framework import serializers

from ..models import Bot, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BotSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Bot
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    # to_bot = serializers.SlugRelatedField(slug_field="name", read_only=True)
    # author_id = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
