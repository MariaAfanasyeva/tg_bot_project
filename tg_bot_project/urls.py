from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views

from mainapp.api import views

from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mainapp.urls")),
    path("api/", include("mainapp.api.urls")),
    path("auth/", include("djoser.urls")),
    path(
        "api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("auth/activate/<uid>/<token>/", views.ActivateUser.as_view(), name="activate"),
]

urlpatterns += doc_urls
