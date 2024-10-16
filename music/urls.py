from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "music"

urlpatterns = [
    path("", TemplateView.as_view(template_name="root.html"), name="root"),  # 기본 루트
    path("index/", views.index, name="index"),  # '/index/' 경로에 index 뷰를 연결
]
