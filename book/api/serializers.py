from rest_framework import serializers

from book.models import Category, Books
from core.models import Request
from notifications.models import TimeLimit


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


class GetBookSerializer(serializers.Serializer):
    dead_line = serializers.IntegerField()

    def validate(self, data):
        user = self.context['user']
        book = self.context['book']
        # meta_data=self.context['meta_data']
        time_limits = TimeLimit.objects.filter(user=user)

        if data['dead_line'] not in [14, 30]:
            raise serializers.ValidationError('شما باید 14 یا 30 روز امانت بگیری')
        # elif Request.objects.filter(user=user, book=book, is_accepted='P', type='B'):
        #     raise serializers.ValidationError('نمیتوانید امانت بگیرید')
        elif time_limits.count() >= 2:
            raise serializers.ValidationError('You cannot take more than two books')
        elif book.stock == 0:
            raise serializers.ValidationError('The book is not available')
        # elif Request.objects.filter(user=user, book=book, type='B').exists():
        #     raise serializers.ValidationError('The approval request for this book has not been approved yet')
        return data


class ExtensionSerializer(serializers.Serializer):
    dead_line = serializers.IntegerField()

    def validate(self, data):
        user = self.context['user']
        book = self.context['book']
        time_limits = TimeLimit.objects.filter(user=user)
        if data['dead_line'] not in [3, 5, 7]:
            raise serializers.ValidationError('شما باید 3و5و7 کتاب را تمدید کنید')
