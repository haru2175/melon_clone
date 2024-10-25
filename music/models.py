from __future__ import annotations
from datetime import date

from typing import Dict
from urllib.parse import quote

from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.utils import timezone


# models.Model 상속
class Song(models.Model):
    melon_uid = models.CharField(max_length=20, unique=False)
    rank = models.PositiveSmallIntegerField(default=0)
    album_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=100)
    cover_url = models.URLField()
    lyrics = models.TextField()
    genre = models.CharField(max_length=100)
    release_date = models.DateField(default=timezone.now)
    like_count = models.PositiveIntegerField(default=0)

    # AI 자작곡 관련 필드 추가
    is_ai_generated = models.BooleanField(default=False)  # AI로 만든 곡 여부
    song_file = models.FileField(
        upload_to="songs/", blank=True, null=True
    )  # 파일 업로드 필드
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )  # 곡 소유자

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


User = get_user_model()  # 현재 사용 중인 사용자 모델 가져오기


# class Playlist(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="playlists",
#     )  # 변경된 related_name
#     name = models.CharField(max_length=100)
#     songs = models.ManyToManyField(
#         "Song", related_name="playlist_songs"
#     )  # 변경된 related_name
#
#     def __str__(self):
#         return self.name
