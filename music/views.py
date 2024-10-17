import json

from django.db.models import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from music.models import Song


def index(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("query", "").strip()

    song_qs: QuerySet[Song] = Song.objects.all()
    # 로컬 JSON 파일 경로
    # melon_chart_path = "C:/workspace/melon_clone/Crawling/melon-20241017.json"

    # # 로컬 JSON 파일 열기
    # with open(melon_chart_path, "r", encoding="utf-8") as json_file:
    #     json_string = json_file.read()
    #
    # # JSON 데이터 파싱 및 Song 객체 생성
    # song_list = [Song.from_dict(song_dict) for song_dict in json.loads(json_string)]

    if query:
        song_qs = song_qs.filter(
            Q(name__icontains=query)
            | Q(artist__icontains=query)
            | Q(album__icontains=query)
        )
        # song_list = [
        #     song
        #     for song in song_list
        #     if query in song.name
        #     or query in song.artist_name
        #     or query in song.album_name
        # ]

    return render(
        request=request,
        template_name="index.html",
        context={
            "song_list": song_qs,
            "query": query,
        },
    )
