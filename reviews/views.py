from django.shortcuts import render
from django.views.generic import TemplateView
from django_filters.views import FilterView
from django.core.paginator import Paginator

from reviews.filters import WorkFilter
from reviews.models import Work


class IndexView(TemplateView):
    template_name = 'index.html'


class SearchResultsView(FilterView):
    model = Work
    template_name = 'search_result.html'
    context_object_name = 'works'
    filterset_class = WorkFilter
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        works = context['page_obj']
        for work in works:
            work.authors_count = work.authors.count()
            if work.authors_count == 1:
                work.single_author = work.authors.first()
        return context

class AboutView(TemplateView):
    template_name = 'about.html'