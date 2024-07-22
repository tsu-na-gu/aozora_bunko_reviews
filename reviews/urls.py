from django.urls import path
from .views import IndexView, SearchResultsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', SearchResultsView.as_view(), name='search'),
]