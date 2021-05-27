from django.urls import path

from . import views

urlpatterns = [
    path("bots", views.GetAllBotsList.as_view(), name="bots"),
    path("detail/<int:pk>", views.GetBotDetail.as_view(), name="detail"),
    path("create", views.CreateBot.as_view(), name="create"),
    path("update/<int:pk>", views.UpdateBot.as_view(), name="update"),
    path("delete/<int:pk>", views.DeleteBot.as_view(), name="delete"),
    path("category", views.GetAllCategoriesList.as_view(), name="categories"),
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
        "bot/<int:pk>/comment/create",
        views.CreateComment.as_view(),
        name="CREATE/comment",
    ),
    path("comment/update/<int:pk>", views.UpdateComment.as_view(), name="PUT/comment"),
    path(
        "comment/delete/<int:pk>", views.DeleteComment.as_view(), name="DELETE/comment"
    ),
]
