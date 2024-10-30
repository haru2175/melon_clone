from django.contrib import admin
from django.utils.html import format_html

from .models import Song
from .utils.melon import get_likes_dict


@admin.register(Song)  # 장식자
class SongAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
        "artist_name",
        "album_name",
    ]  # DB에서는 where 조건으로 검색해서 나오는것!
    list_display = [
        "cover_image",
        "name",
        "artist_name",
        "album_name",
        "genre",
        "like_count_display",
        "release_date",
    ]
    list_filter = ["genre", "release_date"]
    actions = ["update_like_count"]

    def update_like_count(self, request, queryset):
        melon_uid_list = queryset.values_list("melon_uid", flat=True)
        likes_dict = get_likes_dict(melon_uid_list)

        changed_count = 0
        for song in queryset:
            if song.like_count != likes_dict.get(song.melon_uid):
                song.like_count = likes_dict.get(song.melon_uid)
                changed_count += 1

        Song.objects.bulk_update(
            queryset,
            fields=["like_count"],
        )

        self.message_user(request, f"{changed_count} 곡의 좋아요 갱신 완료")

    def cover_image(self, song):
        return format_html(f'<img src="{song.cover_url}" style="width: 50px;"/>')
