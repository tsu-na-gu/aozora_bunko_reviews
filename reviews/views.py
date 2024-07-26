from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django_filters.views import FilterView
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
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

        context['search_query'] = self.request.GET.get('q', '')

        return context


class AboutView(TemplateView):
    template_name = 'about.html'


class BookDetailView(DetailView):
    model = Work
    template_name = 'book_detail.html'
    context_object_name = 'work'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        work = self.get_object()

        authors = work.authors.all()

        authors_wikipedia_links = []

        context['authors'] = work.authors.all()
        context['translator'] = work.translator
        context['editor'] = work.editor
        context['other_role'] = work.other_role
        context['first_publication_info'] = work.first_publication.publication_info if hasattr(work,'first_publication') else None
        context['base_text_info'] = work.base_text_info if hasattr(work, 'base_text_info') else None
        context['genre_info1'] = work.genre_info1.genre if work.genre_info1 else None
        context['genre_info2'] = work.genre_info2.genre if work.genre_info2 else None
        context['authors_count'] = work.authors.count()
        if context['authors_count'] == 1:
            context['single_author'] = context['authors'].first()
        else:
            context['single_author'] = None

        context['page'] = self.request.GET.get('page')

        context['search_query'] = self.request.GET.get('q', None)
        context['reviews'] = work.review_book.all()
        return context