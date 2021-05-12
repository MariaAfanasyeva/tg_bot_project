from rest_framework import serializers

from ..models import Bot, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BotSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Bot
        fields = "__all__"


class BotCategoryDetailSerializer(serializers.ModelSerializer):
    bots = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    @staticmethod
    def get_bots(obj):
        return BotSerializer(Bot.objects.filter(category=obj), many=True).data
