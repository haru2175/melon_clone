import json
from django.utils import timezone

from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView

from music.froms import SongUploadForm
from music.models import Song
from playlist.models import Playlist


class IndexView(ListView):
    model = Song
    template_name = "index.html"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()

        release_date = self.kwargs.get("release_date")
        if release_date:
            qs = qs.filter(release_date=release_date)

        query = self.request.GET.get("query", "").strip()
        if query:
            qs = qs.filter(
                Q(name__icontains=query)
                | Q(artist_name__icontains=query)
                | Q(album_name__icontains=query)
            )

        return qs


index = IndexView.as_view()


def upload_song(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = SongUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():

            song = form.save(commit=False)
            song.artist_name = request.user.username  # 곡 소유자 설정
            song.release_date = timezone.now()  # 현재 날짜 및 시간
            song.is_ai_generated = True  # AI로 만든 곡으로 표시
            song.owner = request.user  # 곡의 소유자를 현재 로그인한 사용자로 설정
            song.save()

            # 업로드한 이미지 파일을 저장
            if request.FILES.get('cover_image'):
                song.cover_image = request.FILES['cover_image']  # 이미지 필드에 파일 저장

            # 선택된 플레이리스트에 곡 추가
            selected_playlist = form.cleaned_data[
                "playlist"
            ]  # 선택된 플레이리스트 가져오기
            selected_playlist.songs.add(song)  # 곡을 선택된 플레이리스트에 추가

            return redirect("playlist:create_playlist")  # 저장 후 리디렉션
    else:
        form = SongUploadForm(user=request.user)
    return render(request, "upload_song.html", {"form": form})
