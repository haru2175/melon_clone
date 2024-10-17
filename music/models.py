from __future__ import annotations

from datetime import date
from typing import Dict
from urllib.parse import quote

from django.db import models


# models.Model 상속
class Song(models.Model):
    melon_uid = models.CharField(max_length=20, unique=True)
    rank = models.PositiveSmallIntegerField()
    album_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=100)
    cover_url = models.URLField()
    lyrics = models.TextField()
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    like_count = models.PositiveIntegerField()

    @property
    def melon_detail_url(self) -> str:
        melon_uid = quote(str(self.melon_uid))
        return f"https://www.melon.com/song/detail.htm?songId={melon_uid}"

    @property
    def youtube_search_url(self) -> str:
        search_query = quote(f"{self.name}, {self.artist_name}")
        return f"https://www.youtube.com/results?search_query={search_query}"

    @classmethod
    def from_dict(cls, data: Dict) -> Song:
        return cls(
            melon_uid=data.get("melon_uid"),
            rank=data.get("rank"),
            album_name=data.get("album_name"),
            name=data.get("name"),
            artist_name=data.get("artist_name"),
            cover_url=data.get("cover_url"),
            lyrics=data.get("lyrics"),
            genre=data.get("장르"),
            release_date=date.fromisoformat(data.get("발매일")),
            like_count=int(data.get("좋아요")),
        )
