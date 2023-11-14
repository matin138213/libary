from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from book.api.permissions import IsAdminSuperUser
from book.api.serializers import CategorySerializer, BookSerializer
from book.models import Category, Books


# Create your views here.
class BookViewSet(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminSuperUser]


class CategoryViewList(ModelViewSet):
    queryset = Category.objects.select_related('parent').all()
    permission_classes = [IsAdminSuperUser]
    serializer_class = CategorySerializer
