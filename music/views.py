from django.db.models import Q
from django.views.generic import ListView

from music.models import Song


class IndexView(ListView):
    model = Song
    template_name = "index.html"
    paginate_by = 9

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

        return qs.order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_range"] = self.get_page_range(context)  # 페이지 범위 추가
        return context

    def get_page_range(self, context):
        """현재 페이지를 기준으로 5페이지 범위를 반환합니다."""
        current_page = self.request.GET.get("page", 1)  # 현재 페이지 번호
        current_page = int(current_page)

        # 페이지 범위 계산
        start_page = max(1, current_page - 2)
        end_page = min(start_page + 4, context["paginator"].num_pages)  # 최대 5페이지

        if end_page - start_page < 4:  # 5페이지 미만일 경우 조정
            start_page = max(1, end_page - 4)

        return range(start_page, end_page + 1)


index = IndexView.as_view()
