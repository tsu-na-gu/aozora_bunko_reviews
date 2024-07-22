from django.shortcuts import render
from django.views.generic import TemplateView
from django_filters.views import FilterView

from reviews.filters import WorkFilter
from reviews.models import Work


class IndexView(TemplateView):
    template_name = 'index.html'


class SearchResultsView(FilterView):
    model = Work
    template_name = 'search_result.html'
    context_object_name = 'works'
    filterset_class = WorkFilter

