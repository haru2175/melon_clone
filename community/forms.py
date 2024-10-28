from django import forms

from community.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post  # Post 모델을 사용한다고 가정
        fields = ["title", "content"]  # 필요한 필드들

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].label = "제목"
        self.fields["content"].label = "내용"
