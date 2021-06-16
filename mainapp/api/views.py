import logging

from django.contrib.auth.models import User
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Bot, Category, Comment, Like
from .paginations import CustomPagination
from .permissions import IsBotAuthor, IsCommentLikeAuthor
from .serializers import (BotSerializer, CategorySerializer, CommentSerializer,
                          LikeSerializer, UserSerializer)

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
    permission_classes = [IsBotAuthor]

    def perform_create(self, serializer):
        serializer.save(add_by_user=self.request.user)


class DeleteBot(generics.DestroyAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    permission_classes = [IsBotAuthor]


class GetAllCategoriesList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GetCategory(generics.RetrieveAPIView):
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


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentLikeAuthor]


# class GetAllLikesToBotList(generics.ListAPIView):
#     serializer_class = LikeSerializer
#     pagination_class = CustomPagination
#
#     def get_queryset(self):
#         bot_id = self.kwargs["pk"]
#         queryset = Comment.objects.filter(to_bot_id=bot_id)
#         return queryset
#
#
# class GetAllCommentsByUserList(generics.ListAPIView):
#     serializer_class = CommentSerializer
#     pagination_class = CustomPagination
#
#     def get_queryset(self):
#         user_id = self.kwargs["pk"]
#         queryset = Comment.objects.filter(author_id=user_id)
#         return queryset


class AddLike(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        current_bot = Bot.objects.get(id=self.kwargs["pk"])
        serializer.save(author=self.request.user, to_bot=current_bot)


class DeleteLike(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsCommentLikeAuthor]
