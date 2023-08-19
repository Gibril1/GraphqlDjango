from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("restaurant.urls")),
    path("auth/", include("accounts.urls")),
]

