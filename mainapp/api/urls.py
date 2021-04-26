from django.urls import path
from . import views

urlpatterns = [
    path('', views.GetAllBotsList.as_view(), name="bots"),
    path('detail/<int:pk>', views.GetBotDetail.as_view(), name="detail"),
    path('create', views.bot_create, name="create"),
    path('update/<int:pk>', views.bot_update, name="update"),
    path('delete/<int:pk>', views.bot_delete, name="delete"),
]
