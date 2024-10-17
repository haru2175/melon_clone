import json

from django.db.models import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from music.models import Song


class IndexView(ListView):
    model = Song
    template_name = "index.html"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()

        release_date = self.kwargs.get("release_date")
        if release_date:
            qs = qs.filter(release_date=release_date)

        query = self.request.GET.get("query", "").strip()
        if query:
            qs = qs.filter(
                Q(name__icontains=query)
                | Q(artist_name__icontains=query)
                | Q(album_name__icontains=query)
            )

        return qs


index = IndexView.as_view()
