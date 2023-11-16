from django.db.models import Count
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from book.api.permissions import IsAdminSuperUser
from book.api.serializers import BookSerializer, SimpleBookSerializer, CategorySerializer
from book.models import Category, Books


# Create your views here.
class BookViewSet(ModelViewSet):
    queryset = Books.objects.prefetch_related('category','category__parent')
    serializer_class = BookSerializer
    permission_classes = [IsAdminSuperUser]

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
