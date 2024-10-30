import json

from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from music.models import Song
from .models import Playlist
from music.froms import SongUploadForm


@login_required
def create_playlist(request):
    # 예시로 첫 번째 Song 객체를 가져온다고 가정
    songs = Song.objects.all()  # 실제 로직에 맞게 수정
    playlists = Playlist.objects.filter(
        user=request.user.id
    )  # 로그인한 유저의 플레이리스트만
    return render(
        request,
        "create_playlist.html",
        {"songs": songs, "playlists": playlists},
    )


def show_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    songs = Song.objects.all()
    return render(
        request,
        "create_playlist.html",
        {"songs": songs, "song": song},
    )


# 노래 추가
def addToPlaylist(request):
    if request.method == "POST":
        data = json.loads(request.body)
        playlist_id = data.get("playlist_id")
        song_id = data.get("song_id")

        user = request.user

        # 플레이리스트와 곡을 가져오기
        playlist = get_object_or_404(Playlist, id=playlist_id, user=user)
        song = get_object_or_404(Song, id=song_id)

        # 디버깅: playlist와 song의 ID 로그 출력
        print(f"User: {user}, Playlist ID: {playlist_id}, Song ID: {song_id}")

        # 플레이리스트에 곡이 이미 있는지 확인
        if playlist.songs.filter(id=song.id).exists():
            return JsonResponse(
                {"status": "error", "message": "해당 곡은 이미 추가되어 있습니다."}
            )

        # 플레이리스트에 곡 추가
        playlist.songs.add(song)

        # 성공 로그 추가
        print(f"Added song: {song.name} to playlist: {playlist.name}")

        return JsonResponse({"status": "success"})  # 성공 시 JSON 응답 반환

    return JsonResponse({"status": "failed"}, status=400)  # 실패 시 JSON 응답 반환


# 노래 삭제
def remove_song_from_playlist(request):
    if request.method == "POST":
        data = json.loads(request.body)
        playlist_id = data.get("playlist_id")
        song_id = data.get("song_id")

        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        song = get_object_or_404(Song, id=song_id)

        # 곡이 플레이리스트에 있는지 확인
        if song not in playlist.songs.all():
            return JsonResponse(
                {"status": "error", "message": "해당 곡은 이미 삭제되었습니다."},
                status=400,
            )

        playlist.songs.remove(song)  # 플레이리스트에서 노래 제거

        return JsonResponse({"status": "success", "message": "곡이 삭제되었습니다."})
    return JsonResponse(
        {"status": "failed", "message": "잘못된 요청입니다."}, status=400
    )


# 좋아요 기능
def like_song(request):
    if request.method == "POST":
        data = json.loads(request.body)
        song_id = data.get("song_id")
        song = get_object_or_404(Song, id=song_id)

        if request.user in song.like_count.all():
            return JsonResponse(
                {"status": "failed", "message": "이미 좋아요를 눌렀습니다."}, status=400
            )

        # 사용자를 좋아요 목록에 추가
        song.like_count.add(request.user)

        # 좋아요 수 반환
        like_count = song.like_count.count()

        return JsonResponse({"status": "success", "like_count": like_count})

    return JsonResponse({"status": "failed"}, status=400)


# 플레이리스트 보기
@login_required
def view_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    # songs = playlist.songs.all()
    return render(request, "view_playlist.html", {"playlist": playlist})


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
                    return redirect("playlist:upload_song")

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
