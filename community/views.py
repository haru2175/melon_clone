from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post
from django.urls import reverse_lazy


class PostListView(ListView):
    model = Post
    template_name = "post_list.html"  # 게시물 목록을 보여줄 템플릿
    context_object_name = "posts"  # 템플릿에서 사용할 객체 이름


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"  # 게시물 상세 페이지 템플릿
    context_object_name = "post"


class PostCreateView(CreateView):
    model = Post
    template_name = "post_form.html"  # 게시물 작성 페이지 템플릿
    fields = ["title", "content"]  # 사용자로부터 받을 필드
    success_url = reverse_lazy("community:post_list")  # 게시물 작성 후 리다이렉트할 URL

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    template_name = "post_form.html"  # 게시물 수정 페이지 템플릿
    fields = ["title", "content"]
    success_url = reverse_lazy("community:post_list")


class PostDeleteView(DeleteView):
    model = Post
    template_name = "post_confirm_delete.html"  # 게시물 삭제 확인 페이지
    success_url = reverse_lazy("community:post_list")
