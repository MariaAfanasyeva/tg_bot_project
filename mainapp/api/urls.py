from django.urls import path

from . import views

urlpatterns = [
    path("bots", views.GetAllBotsList.as_view(), name="bots"),
    path("detail/<int:pk>", views.GetBotDetail.as_view(), name="detail"),
    path("create", views.CreateBot.as_view(), name="create"),
    path("update/<int:pk>", views.UpdateBot.as_view(), name="update"),
    path("delete/<int:pk>", views.DeleteBot.as_view(), name="delete"),
    path("category", views.GetAllCategoriesList.as_view(), name="categories"),
    path("category/<int:pk>", views.GetCategory.as_view(), name="category"),
    path(
        "category/<int:pk>/bots",
        views.GetCategoryDetail.as_view(),
        name="category_detail",
    ),
    path(
        "bot/<int:pk>/comments",
        views.GetAllCommentsToBotList.as_view(),
        name="comments_to_bot",
    ),
    path(
        "user/<int:pk>/comments",
        views.GetAllCommentsByUserList.as_view(),
        name="comments_by_user",
    ),
    path(
        "bot/<int:pk>/comment",
        views.CreateComment.as_view(),
        name="comment_create",
    ),
    path(
        "comment/<int:pk>",
        views.CommentViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="comment_update_delete_retrieve",
    ),
    path("user/<int:id>/bots", views.GetBotsFromUser.as_view(), name="user_bots"),
    path("user/<int:pk>/info", views.GetUser.as_view(), name="user"),
    path("bot/<int:pk>/like", views.AddLike.as_view(), name="add_like"),
    path("like/<int:pk>", views.DeleteLike.as_view(), name="delete_like"),
    path("likes", views.GetAllLikes.as_view(), name="likes list"),
    path(
        "collections",
        views.CollectionViewSet.as_view({"get": "list", "post": "create"}),
        name="collections list or create",
    ),
    path(
        "collection/<int:pk>",
        views.CollectionViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="collection_update_delete_retrieve",
    ),
    path(
        "user/<int:pk>/collections",
        views.GetAllCollectionsByUserList.as_view(),
        name="user_collections",
    ),
]
