from django.urls import path
from .views import IndexView, SearchResultsView, AboutView, BookDetailView, DetailSearchView, DetailSearchResultView, \
    ReviewCreateView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', SearchResultsView.as_view(), name='search_result'),
    path('about/', AboutView.as_view(), name='about'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/<int:book_id>/review/new/', ReviewCreateView.as_view(), name='review_create'),

    path('detail_search/', DetailSearchView.as_view(), name='detail_search'),
    path('detail_search_results/', DetailSearchResultView.as_view(), name='detail_search_results'),
]