from django_filters import rest_framework

from reviews.models import Title


class TitleViewSetFilter(rest_framework.FilterSet):
    category = rest_framework.CharFilter(
        field_name='category__slug',
        lookup_expr='iexact'
    )

    name = rest_framework.CharFilter(
        field_name='name',
        lookup_expr='iexact'
    )

    genre = rest_framework.CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year',)
