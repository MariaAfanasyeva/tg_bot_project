from django.urls import path
from . import views

urlpatterns = [
    path('', views.GetAllBotsList.as_view(), name="bots"),
    path('detail/<int:pk>', views.GetBotDetail.as_view(), name="detail"),
    path('create', views.CreateBot.as_view(), name="create"),
    path('update/<int:pk>', views.UpdateBot.as_view(), name="update"),
    path('delete/<int:pk>', views.DeleteBot.as_view(), name="delete"),
]
