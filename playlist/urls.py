from django.urls import path
from . import views

app_name = "playlist"

urlpatterns = [
    path("create_playlist/", views.create_playlist, name="create_playlist"),
]
