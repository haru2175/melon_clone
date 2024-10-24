import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from music.models import Song
from .models import Playlist


@login_required
def create_playlist(request):
    # 예시로 첫 번째 Song 객체를 가져온다고 가정
    songs = Song.objects.all()  # 실제 로직에 맞게 수정
    playlists = Playlist.objects.filter(
        user=request.user
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

        song.like_count += 1  # 좋아요 수 증가
        song.save()
        return JsonResponse({"status": "success", "like_count": song.like_count})
    return JsonResponse({"status": "failed"}, status=400)


# 플레이리스트 보기
@login_required
def view_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    songs = playlist.songs.all()
    return render(request, "view_playlist.html", {"playlist": playlist})


# def playlist_view(request):
#     if request.user.is_authenticated:  # 유저가 로그인했는지 확인
#         playlists = Playlist.objects.filter(
#             user=request.user
#         )  # 로그인한 유저의 플레이리스트만 가져오기
#     else:
#         playlists = None  # 로그인하지 않았다면 아무 플레이리스트도 없음
#
#     return render(request, "create_playlist.html", {"playlists": playlists})
