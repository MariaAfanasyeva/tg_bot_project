from ..models import Bot, Category
from .serializers import BotSerializer, CategorySerializer, BotCategoryDetailSerializer
import logging
from rest_framework import generics

logger = logging.getLogger(__name__)


class GetAllBotsList(generics.ListAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer


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


class GetCategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = BotCategoryDetailSerializer

