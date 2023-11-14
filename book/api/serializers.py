from rest_framework import serializers

from book.models import Category, Books


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['id','owner', 'publisher', 'vol', 'page_count', 'writer', 'translator', 'publish_year', 'stock', 'title',
                  'description', 'picture','evable_notif']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title', 'parent', 'book']
