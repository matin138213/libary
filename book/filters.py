# from django_filters import IsoDateTimeFilter
from django_filters.rest_framework import FilterSet
from .models import Books, Category


class BooksFilter(FilterSet):
    class Meta:
        model = Books
        fields = {
            'category': ['exact'],
            'stock':['exact'],
        }
