from django.urls import path
from .views import IndexView, SearchResultsView, AboutView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('about/', AboutView.as_view(), name='about'),
]