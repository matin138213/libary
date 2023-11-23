import re

from rest_framework import serializers

from book.models import Books
from core.models import Users, Request
from django.contrib.auth.hashers import check_password, make_password

apps_name = 'core'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, data):
        username = data['username']
        password = data['password']

        user = Users.objects.filter(username=username).first()
        if not user:
            raise serializers.ValidationError('Username does not exist')
        if not check_password(password, user.password):
            raise serializers.ValidationError('Invalid password')

        return data


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ['id', 'first_name', 'confirm_password', 'last_name', 'email', 'phone_number', 'telegram_id',
                  'password', 'username']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('password yeki nist')
        pattern = r'^09[0-9]{9}$'  # re to argoman
        if not re.match(pattern, data['phone_number']):
            raise serializers.ValidationError("شماره موبایل نامعتبر هست")
        telegram_id = data['telegram_id']
        if any('\u0600' <= char <= '\u06FF' for char in telegram_id):
            raise serializers.ValidationError("Telegram ID should not contain Farsi letters.")
        return data


class RequestBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['id', 'title', 'picture']


class UsersSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['id', 'full_name']

    def get_full_name(self, obj):
        return obj.get_full_name()


class RequestSerializer(serializers.ModelSerializer):
    book = RequestBookSerializer()
    user = UsersSerializer()

    class Meta:
        model = Request
        fields = ['id', 'book', 'user', 'created_at', 'meta_data', 'type', 'is_accepted']


class SimpleRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['is_accepted']
