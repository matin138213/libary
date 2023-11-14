from django.urls import path, include
from . import api_views
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('category', api_views.CategoryViewList, basename='category'),
router.register('books', api_views.BookViewSet, basename='books'),
urlpatterns = router.urls