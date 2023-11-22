from django.db.models import Count, Q, Avg, Value
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from book.api.permissions import IsAdminSuperUser
from book.api.serializers import BookSerializer, SimpleBookSerializer, CategorySerializer
from book.filters import BooksFilter
from book.models import Category, Books
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.functions import Coalesce
from django.db.models import IntegerField

class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsAdminSuperUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['borrow_count', 'created_at', 'popular']
    search_fields = ['writer', 'title']
    filterset_class = BooksFilter

    def get_queryset(self):
        queryset = Books.objects.prefetch_related('category').all()
        queryset = queryset.annotate(
            borrow_count=Count('request', filter=Q(request__type='B', request__is_accepted='A')),
            popular=Coalesce(Avg('comment__star', output_field=IntegerField()), Value(0))
        )

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SimpleBookSerializer
        elif self.request.method == 'GET':
            return BookSerializer
        return BookSerializer


class CategoryViewList(ModelViewSet):
    queryset = Category.objects.select_related('parent').all()
    permission_classes = [IsAdminSuperUser]
    filterset_fields = ['parent']
    filter_backends = [DjangoFilterBackend]
    serializer_class = CategorySerializer
