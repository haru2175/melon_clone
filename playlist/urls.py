from django.urls import path
from . import views

app_name = "playlist"

urlpatterns = [
    path("create_playlist/", views.create_playlist, name="create_playlist"),
    path("song/<int:song_id>/", views.show_song, name="show_song"),
    path("add_song/", views.addToPlaylist, name="addToPlaylist"),
    path(
        "remove_song/",
        views.remove_song_from_playlist,
        name="remove_song_from_playlist",
    ),
    path("view/<int:playlist_id>/", views.view_playlist, name="view_playlist"),
    path("like_song/", views.like_song, name="like_song"),
]
