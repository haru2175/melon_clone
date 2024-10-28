from django.db import models
from django.conf import settings  # AUTH_USER_MODEL 사용을 위한 import


class Post(models.Model):
    # 게시물의 제목, 최대 200자까지 허용
    title = models.CharField(max_length=200)
    # 게시물의 내용을 저장하는 필드
    content = models.TextField()
    # 게시물 작성자: User 모델과 연결 (외래 키)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 게시물이 생성된 날짜와 시간 자동으로 추가
    created_at = models.DateTimeField(auto_now_add=True)
    # 게시물이 수정된 날짜와 시간 자동으로 업데이트
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # 게시물의 제목을 문자열로 반환
        return self.title


class Comment(models.Model):
    # 어떤 게시물에 대한 댓글인지 연결 (외래 키)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    # 댓글의 내용을 저장하는 필드
    content = models.TextField()
    # 댓글 작성자: User 모델과 연결 (외래 키)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 댓글이 생성된 날짜와 시간 자동으로 추가
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # 댓글 작성자와 게시물 제목을 포함한 문자열 반환
        return f"Comment by {self.author} on {self.post}"


class PostLike(models.Model):
    # 좋아요를 누른 게시물과 연결 (외래 키)
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    # 좋아요를 누른 사용자: User 모델과 연결 (외래 키)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        # 같은 게시물에 같은 사용자가 좋아요를 여러 번 누르지 못하도록 제한
        unique_together = ("post", "user")
