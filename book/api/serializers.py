from rest_framework import serializers

from book.models import Category, Books


# class SimpleCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'title','parent']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'parent']


class ParentCategorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'parent',
        ]

    def get_parent(self, obj):
        try:
            if obj.parent:
                serializer = ParentCategorySerializer(obj.parent, context=self.context)
                return serializer.data
        except Exception:
            return None


class SimpleBookSerializer(serializers.ModelSerializer):
    # parent = CategorySerializer()

    class Meta:
        model = Books
        fields = ['id', 'owner', 'publisher', 'vol', 'page_count', 'writer', 'translator', 'publish_year', 'stock',
                  'title', 'description', 'picture', 'category']


class BookSerializer(serializers.ModelSerializer):
    category = ParentCategorySerializer(many=True)

    class Meta:
        model = Books
        fields = ['id', 'owner', 'publisher', 'vol', 'page_count', 'writer', 'translator', 'publish_year', 'stock',
                  'title', 'description', 'picture', 'category']
