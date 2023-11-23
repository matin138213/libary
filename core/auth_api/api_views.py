from django.shortcuts import render
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from core.auth_api.permissions import IsAdminSuperUser
from core.auth_api.serializers import LoginSerializer, UserSerializer, LogoutSerializer, RequestSerializer, \
    SimpleRequestSerializer
from core.models import Users, Request


# Create your views here.


class Login(CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data['username']
        password = serializer.data['password']
        user = Users.objects.get(username=username)

        refresh = RefreshToken.for_user(user)
        response = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        headers = self.get_success_headers(serializer.data)

        return Response(response, status=status.HTTP_201_CREATED, headers=headers)


class LogoutView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def create(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminSuperUser]

    @action(detail=False, methods=['GET', 'PATCH'], permission_classes=[IsAuthenticated],
            serializer_class=UserSerializer)
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class RequestViewSet(ListModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet, RetrieveModelMixin):
    queryset = Request.objects.select_related('book','user').all()
    permission_classes = [IsAdminSuperUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_accepted','type']

    def get_serializer_class(self):
        if self.request.method in ['PATCH','PUT']:
            return SimpleRequestSerializer
        return RequestSerializer
