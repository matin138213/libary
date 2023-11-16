from django.urls import path, include
from . import api_views
from rest_framework_nested import routers

app_name = 'core'

router = routers.DefaultRouter()
router.register('users', api_views.UserViewSet, basename='users')

urlpatterns = [
    path('login/', api_views.Login.as_view(), name='login'),
    path('logout/', api_views.LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
