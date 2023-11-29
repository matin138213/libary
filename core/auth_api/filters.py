from django_filters.rest_framework import FilterSet
from core.models import Request


class RequestFilter(FilterSet):
    class Meta:
        model = Request
        fields = {
            'created_at': ['lte', 'gte'],
            'type': ['exact'],
            'is_accepted': ['exact'],
        }
