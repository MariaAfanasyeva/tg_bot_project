from django.contrib import admin
from django.urls import include, path

from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mainapp.urls")),
    path("api/", include("mainapp.api.urls")),
]

urlpatterns += doc_urls
