from django.contrib import admin
from .models import Post, Comment

# Post 모델 등록
admin.site.register(Post)

# Comment 모델 등록
admin.site.register(Comment)