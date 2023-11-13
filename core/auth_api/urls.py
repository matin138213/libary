from rest_framework.urls import path
from . import api_views

urlpatterns = [
    path('login/', api_views.Login.as_view()),
]