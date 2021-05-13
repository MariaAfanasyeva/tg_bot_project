import logging

from rest_framework import filters, generics

from ..models import Bot, Category
from .paginations import CustomPagination
from .serializers import BotSerializer, CategorySerializer

logger = logging.getLogger(__name__)


class GetAllBotsList(generics.ListAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description", "category__name"]


class GetBotDetail(generics.RetrieveAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer


class CreateBot(generics.CreateAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer


class UpdateBot(generics.UpdateAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer


class DeleteBot(generics.DestroyAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer


class GetAllCategoriesList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GetCategoryDetail(generics.ListAPIView):
    serializer_class = BotSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        category = self.kwargs["pk"]
        queryset = Bot.objects.filter(category_id=category)
        return queryset
