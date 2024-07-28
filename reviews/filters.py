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


class DetailSearchFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title', lookup_expr='icontains', label='書籍名'
    )
    title_reading = django_filters.CharFilter(
        field_name='title_reading', lookup_expr='icontains', label='書籍名（読み）'
    )
    author_last_name = django_filters.CharFilter(
        field_name='authors__last_name', lookup_expr='icontains', label='著者の姓'
    )
    author_first_name = django_filters.CharFilter(
        field_name='authors__first_name', lookup_expr='icontains', label='著者の名'
    )
    author_last_name_reading = django_filters.CharFilter(
        field_name='authors__last_name_reading', lookup_expr='icontains', label='著者の姓（読み）'
    )
    author_first_name_reading = django_filters.CharFilter(
        field_name='authors__first_name_reading', lookup_expr='icontains', label='著者の名（読み）'
    )
    translator_last_name = django_filters.CharFilter(
        field_name='translator__last_name', lookup_expr='icontains', label='翻訳者の姓'
    )
    translator_first_name = django_filters.CharFilter(
        field_name='translator__first_name', lookup_expr='icontains', label='翻訳者の名'
    )
    translator_last_name_reading = django_filters.CharFilter(
        field_name='translator__last_name_reading', lookup_expr='icontains', label='翻訳者の姓（読み）'
    )
    translator_first_name_reading = django_filters.CharFilter(
        field_name='translator__first_name_reading', lookup_expr='icontains', label='翻訳者の名（読み）'
    )
    character_usage = django_filters.ChoiceFilter(
        field_name='character_usage',
        choices=[
            ('新字旧仮名', '新字旧仮名'),
            ('旧字旧仮名', '旧字旧仮名'),
            ('新字新仮名', '新字新仮名'),
        ],
        label='仮名遣い'
    )

    class Meta:
        model = Work
        fields = [
            'title', 'title_reading', 'author_last_name', 'author_first_name',
            'author_last_name_reading', 'author_first_name_reading',
            'translator_last_name', 'translator_first_name',
            'character_usage'
        ]