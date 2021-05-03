from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='homePage'),
    path('category/<int:id>', views.category_detail, name='category_detail')
]
