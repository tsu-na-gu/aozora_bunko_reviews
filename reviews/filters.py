import django_filters
from django.db.models import Q

from reviews.models import Work


class WorkFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='filter_by_all_fields',
        label= "検索フィールド"
    )

    ordering = django_filters.OrderingFilter(
        fields = (
            ('title_sorting', 'title_sorting')
        ),
        label='並び替え',
        field_labels={
            'title_sorting': '作品名'
        }
    )

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
                    Q(authors__last_name__icontains=term) |
                    Q(authors__first_name__icontains=term) |
                    Q(authors__last_name_reading__icontains=term) |
                    Q(authors__first_name_reading__icontains=term) |
                    Q(authors__full_name__icontains=term) |
                    Q(authors__full_name_reading__icontains=term) |
                    Q(translator__last_name__icontains=term) |
                    Q(translator__first_name__icontains=term) |
                    Q(translator__last_name_reading__icontains=term) |
                    Q(translator__first_name_reading__icontains=term) |
                    Q(translator__full_name__icontains=term) |
                    Q(translator__full_name_reading__icontains=term) |
                    Q(editor__last_name__icontains=term) |
                    Q(editor__first_name__icontains=term) |
                    Q(editor__last_name_reading__icontains=term) |
                    Q(editor__first_name_reading__icontains=term) |
                    Q(editor__full_name__icontains=term) |
                    Q(editor__full_name_reading__icontains=term) |
                    Q(other_role__last_name__icontains=term) |
                    Q(other_role__first_name__icontains=term) |
                    Q(other_role__last_name_reading__icontains=term) |
                    Q(other_role__first_name_reading__icontains=term) |
                    Q(other_role__full_name__icontains=term) |
                    Q(other_role__full_name_reading__icontains=term)
            )
            query &= term_query

        return queryset.filter(query).distinct()
