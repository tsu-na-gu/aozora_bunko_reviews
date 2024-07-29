from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView, FormView, CreateView
from django_filters.views import FilterView
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from account.models import ReviewHistory
from reviews.filters import WorkFilter, DetailSearchFilter
from reviews.forms import DetailSearchForm, ReviewForm
from reviews.models import Work, Review
from django.utils.html import escape
from reviews.utils import SearchHistoryManager, keep_latest_page_param


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        show_success_dialog = self.request.GET.get('new_user') == 'true'
        context['show_success_dialog'] = show_success_dialog

        return context


class SearchResultsView(FilterView):
    model = Work
    template_name = 'search_result.html'
    context_object_name = 'works'
    filterset_class = WorkFilter
    paginate_by = 10
    search_history_manager = SearchHistoryManager()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        works = context['page_obj']
        for work in works:
            work.authors_count = work.authors.count()
            if work.authors_count == 1:
                work.single_author = work.authors.first()

        search_query = keep_latest_page_param(self.request.GET.urlencode())
        context['search_query'] = escape(search_query)

        # 'page' パラメータがない場合のみ検索履歴に保存
        self.search_history_manager.save_search_history(self.request.user, self.request)

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

        search_query = keep_latest_page_param(self.request.GET.urlencode())
        context['search_query'] = escape(search_query)
        context['reviews'] = work.review_book.all()
        return context


class DetailSearchView(FormView):
    template_name = 'detail_search.html'
    form_class = DetailSearchForm

    def form_valid(self, form):
        query_params = form.cleaned_data
        query_params['q'] = 'detail_search'  # クエリにqパラメータを追加
        query_string = "&".join([f"{key}={value}" for key, value in query_params.items() if value])
        return redirect(f"{reverse('detail_search_results')}?{query_string}")


class DetailSearchResultView(FilterView):
    model = Work
    template_name = 'detail_search_result.html'
    context_object_name = 'works'
    filterset_class = DetailSearchFilter
    paginate_by = 10
    search_history_manager = SearchHistoryManager()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        works = context['page_obj']
        for work in works:
            work.authors_count = work.authors.count()
            if work.authors_count == 1:
                work.single_author = work.authors.first()

        context['search_query'] = keep_latest_page_param(self.request.GET.urlencode())

        # 'page' パラメータがない場合のみ検索履歴に保存
        self.search_history_manager.save_search_history(self.request.user, self.request)

        return context

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        book_id = self.kwargs.get('book_id')
        book = get_object_or_404(Work, pk=book_id)
        form.instance.book = book
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs.get('book_id')
        context["book"] = get_object_or_404(Work, pk=book_id)
        search_query = keep_latest_page_param(self.request.GET.urlencode())
        context['search_query'] = escape(search_query)

        return context

    def get_success_url(self):
        search_query = escape(self.request.GET.urlencode())
        if search_query:
            return f"{reverse('book_detail', kwargs={'pk': self.object.book.pk})}?{search_query}"
        return reverse('book_ditail', kwargs={'pk' : self.object.book.pk})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)

        ReviewHistory.objects.create(
            user = self.request.user,
            review=form.instance,
            review_url=reverse('book_detail', kwargs={'pk': form.instance.book.pk}),
        )

        return response


