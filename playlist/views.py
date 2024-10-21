from django.shortcuts import render, get_object_or_404
from music.models import Song


def create_playlist(request):
    # 예시로 첫 번째 Song 객체를 가져온다고 가정
    songs = Song.objects.all()  # 실제 로직에 맞게 수정
    return render(
        request,
        "create_playlist.html",
        {"songs": songs},
    )


def show_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    songs = Song.objects.all()
    return render(request, "create_playlist.html", {"songs": songs, "song": song})
