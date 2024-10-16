from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Dict
from urllib.parse import quote


# 파이썬 3.7부터 지원
@dataclass
class Song:
    id: str
    rank: int
    album_name: str
    name: str
    artist_name: str
    cover_url: str
    lyrics: str
    genre: str
    release_date: date
    like_count: int

    @property
    def melon_detail_url(self) -> str:
        melon_uid = quote(str(self.id))
        return f"https://www.melon.com/song/detail.htm?songId={melon_uid}"

    @property
    def youtube_search_url(self) -> str:
        search_query = quote(f"{self.name}, {self.artist_name}")
        return f"https://www.youtube.com/results?search_query={search_query}"

    @classmethod
    def from_dict(cls, data: Dict) -> Song:
        return cls(
            id=data.get("id"),
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
