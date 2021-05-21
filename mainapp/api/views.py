import logging

from rest_framework import filters, generics

from ..models import Bot, Category, Comment
from .paginations import CustomPagination
from .serializers import BotSerializer, CategorySerializer, CommentSerializer

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
        bot = self.kwargs["pk"]
        queryset = Comment.objects.filter(to_bot_id=bot)
        return queryset


class GetAllCommentsByUserList(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.kwargs["pk"]
        queryset = Comment.objects.filter(author_id=user)
        return queryset


class CreateComment(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class UpdateComment(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class DeleteComment(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
