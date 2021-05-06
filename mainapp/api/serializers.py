from django.core.paginator import Paginator
from rest_framework import serializers
from ..models import Bot, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class BotSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Bot
        fields = '__all__'


class BotCategoryDetailSerializer(serializers.ModelSerializer):
    bots = serializers.SerializerMethodField('paginated_bots')

    class Meta:
        model = Category
        fields = '__all__'

    @staticmethod
    def get_bots(obj):
        print(obj)
        return BotSerializer(Bot.objects.filter(category=obj), many=True).data

    def paginated_bots(self, obj):
        page_size = self.context['request'].query_params.get('size') or 10
        bots = Bot.objects.filter(category=obj)
        paginator = Paginator(bots, page_size)
        page = self.context['request'].query_params.get('page') or 1

        words_in_book = paginator.page(page)
        serializer = BotSerializer(words_in_book, many=True)

        return serializer.data


