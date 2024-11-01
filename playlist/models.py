from django.db import models
from django.conf import settings  # AUTH_USER_MODEL 사용을 위한 import


class Playlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="playlist",
    )  # 변경된 related_name
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(
        "music.Song", related_name="playlist"
    )  # 변경된 related_name

    def __str__(self):
        return self.name

    # self 인스턴스 변수를 쓰기 위해서 쓰는것.
