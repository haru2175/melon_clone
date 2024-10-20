from django.shortcuts import render
from music.models import Song


def create_playlist(request):
    # 예시로 첫 번째 Song 객체를 가져온다고 가정
    song = Song.objects.first()  # 실제 로직에 맞게 수정
    return render(
        request,
        "create_playlist.html",
        {"song": song},
    )
