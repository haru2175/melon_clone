import json
from urllib.request import urlopen

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from music.models import Song


def index(request: HttpRequest) -> HttpResponse:
    # 로컬 JSON 파일 경로
    melon_chart_path = "C:/workspace/melon_clone/Crawling/melon-20241016.json"

    # 로컬 JSON 파일 열기
    with open(melon_chart_path, "r", encoding="utf-8") as json_file:
        json_string = json_file.read()

    # JSON 데이터 파싱 및 Song 객체 생성
    song_list = [Song.from_dict(song_dict) for song_dict in json.loads(json_string)]

    return render(
        request=request,
        template_name="index.html",
        context={
            "song_list": song_list,
        },
    )
