import django_filters
from django.db.models import Q

from reviews.models import Work


class WorkFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='filter_by_all_fields')

    class Meta:
        model = Work
        fields = []

    def filter_by_all_fields(self, queryset, name, value):
        terms = value.split()
        query = Q()
        for term in terms:
            term_query = (
                    Q(title__icontains=term) |
                    Q(sub_title__icontains=term) |
                    Q(title_reading__icontains=term) |
                    Q(author__last_name__icontains=term) |
                    Q(author__first_name__icontains=term) |
                    Q(author__last_name_reading__icontains=term) |
                    Q(author__first_name_reading__icontains=term)
            )
            query &= term_query

        return queryset.filter(query).distinct()
