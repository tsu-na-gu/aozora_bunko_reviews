from django.urls import path
from .views import IndexView, SearchResultsView, AboutView, BookDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', SearchResultsView.as_view(), name='search_result'),
    path('about/', AboutView.as_view(), name='about'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
]