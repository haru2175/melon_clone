from django.core.exceptions import PermissionDenied
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post, Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator


class PostListView(ListView):
    model = Post
    template_name = "post_list.html"  # 게시물 목록을 보여줄 템플릿
    context_object_name = "posts"  # 템플릿에서 사용할 객체 이름
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"  # 게시물 상세 페이지 템플릿
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["content"]  # 댓글 내용
    success_url = reverse_lazy(
        "community:post_comment"
    )  # 댓글 작성 후 리다이렉트할 URL

    def get_success_url(self):
        return reverse("community:post_detail", kwargs={"pk": self.kwargs["post_id"]})

    def form_valid(self, form):
        form.instance.author = self.request.user  # 현재 사용자 설정
        form.instance.post = get_object_or_404(
            Post, pk=self.kwargs["post_id"]
        )  # 해당 게시물 설정
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        # 삭제 후 현재 게시물의 상세 페이지로 리다이렉트
        return reverse_lazy(
            "community:post_detail", kwargs={"pk": self.kwargs["post_id"]}
        )

    def get_object(self, queryset=None):
        post_id = self.kwargs.get("post_id")
        comment_id = self.kwargs.get("comment_id")
        # 댓글을 가져오기 위해 get_object_or_404 사용
        comment = get_object_or_404(Comment, pk=comment_id, post_id=post_id)
        # 현재 사용자와 댓글 작성자가 같지 않으면 PermissionDenied
        if comment.author != self.request.user:
            raise PermissionDenied
        return comment
