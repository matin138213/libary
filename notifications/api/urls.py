from django.urls import path, include
from . import api_views
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('notif', api_views.NotificationsViewSet, basename='notif'),
# router.register('request',api_views.RequestViewSet,basename='request'),
urlpatterns = router.urls