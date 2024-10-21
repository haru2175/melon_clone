from django.db import models


class Song(models.Model):
    name = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    cover_url = models.URLField()

    def __str__(self):
        return self.name


class Playlist(models.Model):
    name = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.name
