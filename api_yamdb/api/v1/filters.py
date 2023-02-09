from rest_framework import filters
from reviews.models import Title


class TitleFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        queryset = Title.objects.all()
        category = request.query_params.get('category')
        genre = request.query_params.get('genre')
        name = request.query_params.get('name')
        year = request.query_params.get('year')
        if category is not None:
            return queryset.filter(category__slug=category)
        if genre is not None:
            return queryset.filter(genre__slug=genre)
        if year is not None:
            return queryset.filter(year=year)
        if name is not None:
            return queryset.filter(name=name)
        return queryset
