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
    path("user/<int:id>/bots", views.GetBotsFromUser.as_view(), name="user_bots"),
]
