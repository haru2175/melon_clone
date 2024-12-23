from django.apps import apps
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("playlist/", include("playlist.urls")),
    path("comments/", include("community.urls")),
    path("", include("music.urls")),
]


if apps.is_installed("debug_toolbar"):
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
