from rest_framework import serializers

from core.models import Users
from django.contrib.auth.hashers import check_password


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    # def validate(self, data):
    #     password = data['password']
    #     if not Users.objects.filter(username=data['username']).exists():
    #         raise serializers.ValidationError('Username does not exist')
    #     if not check_password(password,user.password):
    #         raise serializers.ValidationError('Invalid password')
    #     return data
    def validate(self, data):
        username = data['username']
        password = data['password']

        user = Users.objects.filter(username=username).first()
        if not user:
            raise serializers.ValidationError('Username does not exist')
        if not check_password(password, user.password):
            raise serializers.ValidationError('Invalid password')

        return data





