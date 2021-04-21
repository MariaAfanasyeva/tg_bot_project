from django.urls import path
from . import views

urlpatterns = [
    path('', views.bots_list, name="bots"),
    path('detail/<str:pk>', views.bot_detail, name="detail"),
    path('create', views.bot_create, name="create"),
    path('update/<str:pk>', views.bot_update, name="update"),
    path('delete/<str:pk>', views.bot_delete, name="delete"),
]
