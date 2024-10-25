from django.conf import settings  # settings 파일을 가져온다.
from django.conf.urls.static import (
    static,
)  # static 함수는 미디어 URL 패턴을 추가하는데 사용됩니다
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "music"

urlpatterns = [
    path("", TemplateView.as_view(template_name="root.html"), name="root"),  # 기본 루트
    path("index/", views.index, name="index"),  # '/index/' 경로에 index 뷰를 연결
    path("upload_song/", views.upload_song, name="upload_song"),
]

# MEDIA_URL 경로 설정 추가
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
