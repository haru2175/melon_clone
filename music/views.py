from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView

from music.froms import SongUploadForm
from music.models import Song


class IndexView(ListView):
    model = Song
    template_name = "index.html"
    paginate_by = 9

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

        return qs.order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_range"] = self.get_page_range(context)  # 페이지 범위 추가
        return context

    def get_page_range(self, context):
        """현재 페이지를 기준으로 5페이지 범위를 반환합니다."""
        current_page = self.request.GET.get("page", 1)  # 현재 페이지 번호
        current_page = int(current_page)

        # 페이지 범위 계산
        start_page = max(1, current_page - 2)
        end_page = min(start_page + 4, context["paginator"].num_pages)  # 최대 5페이지

        if end_page - start_page < 4:  # 5페이지 미만일 경우 조정
            start_page = max(1, end_page - 4)

        return range(start_page, end_page + 1)


index = IndexView.as_view()


def upload_song(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = SongUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            # 파일 확장자 검증
            song_file = request.FILES.get("song_file")
            if song_file:
                allowed_extensions = ["jpg", "png"]
                file_extension = song_file.name.split(".")[-1].lower()

                if file_extension not in allowed_extensions:
                    # 확장자가 허용되지 않으면 오류 메시지 반환
                    messages.error(
                        request,
                        "이미지 파일 형식이 아닙니다. .jpg 또는 .png 파일만 업로드해주세요.",
                    )
                    return redirect("music:upload_song")

            song = form.save(commit=False)
            song.artist_name = request.user.username  # 곡 소유자 설정
            song.release_date = timezone.now()  # 현재 날짜 및 시간
            song.is_ai_generated = True  # AI로 만든 곡으로 표시
            song.owner = request.user  # 곡의 소유자를 현재 로그인한 사용자로 설정
            song.save()

            # 선택된 플레이리스트에 곡 추가
            selected_playlist = form.cleaned_data[
                "playlist"
            ]  # 선택된 플레이리스트 가져오기
            selected_playlist.songs.add(song)  # 곡을 선택된 플레이리스트에 추가

            return redirect("playlist:create_playlist")  # 저장 후 리디렉션
    else:
        form = SongUploadForm(user=request.user)
    return render(request, "upload_song.html", {"form": form})
