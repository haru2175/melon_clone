from django.urls import path
from django.views.generic import TemplateView


app_name = "music"

urlpatterns = [
    path("", TemplateView.as_view(template_name="root.html"), name="root"),
]
