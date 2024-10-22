import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from music.models import Song
from .models import Playlist


def create_playlist(request):
    # 예시로 첫 번째 Song 객체를 가져온다고 가정
    songs = Song.objects.all()  # 실제 로직에 맞게 수정
    playlists = Playlist.objects.all()
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

        playlist = get_object_or_404(Playlist, id=playlist_id)
        song = get_object_or_404(Song, id=song_id)

        playlist.songs.add(song)  # 플레이리스트에 노래 추가
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)


# 노래 삭제
def remove_song_from_playlist(request):
    if request.method == "POST":
        data = json.loads(request.body)
        playlist_id = data.get("playlist_id")
        song_id = data.get("song_id")

        playlist = get_object_or_404(Playlist, id=playlist_id)
        song = get_object_or_404(Song, id=song_id)

        playlist.songs.remove(song)  # 플레이리스트에서 노래 제거
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)


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
def view_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    return render(request, "view_playlist.html", {"playlist": playlist})
