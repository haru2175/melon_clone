from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),  # 게시물 목록 페이지
    path(
        "post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"
    ),  # 게시물 상세 페이지
    path(
        "post/new/", views.PostCreateView.as_view(), name="post_create"
    ),  # 새 게시물 작성 페이지
    path(
        "post/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_edit"
    ),  # 게시물 수정 페이지
    path(
        "post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"
    ),  # 게시물 삭제 페이지
]
