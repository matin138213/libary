from datetime import timedelta, datetime

from django.shortcuts import render
from django.utils import timezone
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

from book.models import Books
from core.auth_api.filters import RequestFilter
from core.auth_api.permissions import IsAdminSuperUser
from core.auth_api.serializers import LoginSerializer, UserSerializer, LogoutSerializer, RequestSerializer, \
    SimpleRequestSerializer
from core.models import Users, Request
from notifications.models import Notifications, TimeLimit
from rest_framework import status


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
    queryset = Request.objects.all().order_by('-created_at')
    permission_classes = [IsAdminSuperUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RequestFilter

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return SimpleRequestSerializer
        return RequestSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        instance = self.get_object()
        instance_accepted = instance.is_accepted
        days = int(instance.meta_data)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if instance.is_accepted == 'A':
            book = instance.book
            print("Before decrease: ", book.stock)
            book.stock -= 1
            print("After decrease: ", book.stock)
            book.save()
            print("Book ID: ", instance.book.id)

        if instance.is_accepted == 'A':
            user = self.request.user

            book = instance.book
            notifications = Notifications.objects.create(user=user,
                                                         description=f'{book.title}درخواست امانت برای این کتاب تایید شد',
                                                         title='تاییدشد', picture=book.picture)
            end_time = datetime.now() + timedelta(days=int(days))
            time_limit = TimeLimit.objects.create(user=user, book=book, end_time=end_time)
        elif instance.is_accepted == 'N':
            user = self.request.user
            book = instance.book
            notifications = Notifications.objects.create(user=user,
                                                         description=f'{book.title}درخواست امانت برای این کتاب رد شد',
                                                         title='ردشد', picture=book.picture)

        return Response(serializer.data, status=status.HTTP_200_OK)
