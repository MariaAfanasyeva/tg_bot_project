import logging

from django.contrib.auth.models import User
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from ..models import Bot, Category, Comment
from .paginations import CustomPagination
from .serializers import (BotSerializer, CategorySerializer, CommentSerializer,
                          UserSerializer)

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


class GetAllCommentsToBotList(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        bot_id = self.kwargs["pk"]
        queryset = Comment.objects.filter(to_bot_id=bot_id)
        return queryset


class GetAllCommentsByUserList(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user_id = self.kwargs["pk"]
        queryset = Comment.objects.filter(author_id=user_id)
        return queryset


class CreateComment(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        current_bot = Bot.objects.get(id=self.kwargs["pk"])
        serializer.save(author=self.request.user, to_bot=current_bot)


class UpdateComment(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class DeleteComment(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class GetUser(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User
