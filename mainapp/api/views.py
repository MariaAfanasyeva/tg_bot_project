import logging

from django.contrib.auth.models import User
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from ..models import Bot, Category
from .paginations import CustomPagination
from .permissions import IsAuthor
from .serializers import BotSerializer, CategorySerializer, UserSerializer

logger = logging.getLogger(__name__)


class GetAllBotsList(generics.ListAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description", "category__name", "author"]


class GetBotDetail(generics.RetrieveAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer


class CreateBot(generics.CreateAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(add_by_user=self.request.user)


class UpdateBot(generics.UpdateAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    permission_classes = [IsAuthor]

    def perform_create(self, serializer):
        serializer.save(add_by_user=self.request.user)


class DeleteBot(generics.DestroyAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    permission_classes = [IsAuthor]


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


class GetBotsFromUser(generics.ListAPIView):
    serializer_class = BotSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user_id = self.kwargs["id"]
        queryset = Bot.objects.filter(add_by_user=user_id)
        return queryset


class GetUser(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User
