from django.db import models
from django.conf import settings


class Playlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)


class Song(models.Model):
    playlist = models.ForeignKey(
        Playlist, related_name="songs", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
