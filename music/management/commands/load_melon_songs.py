import json

from django.core.management import BaseCommand

from music.models import Song


class Command(BaseCommand):
    help = "Load songs from melon chart"

    def handle(self, *args, **options):
        # 로컬 JSON 파일 경로
        melon_chart_path = "C:/workspace/melon_clone/Crawling/melon-20241017.json"

        # 로컬 JSON 파일 열기
        with open(melon_chart_path, "r", encoding="utf-8") as json_file:
            json_string = json_file.read()

        # Song 인스턴스들은 아직 데이터베이스에 저장되지 않았습니다.
        song_list = [Song.from_dict(song_dict) for song_dict in json.loads(json_string)]
        print("loaded song_list :", len(song_list))

        # Song 인스턴스들은 한 번에 INSERT 쿼리를 생성하여, INSERT 성능을 높입니다.
        Song.objects.bulk_create(song_list, batch_size=100, ignore_conflicts=True)

        total = Song.objects.all().count()
        print("saved song_list :", total)
