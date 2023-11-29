from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from book.api.permissions import IsAdminSuperUser
from notifications.api.serializers import NotificationsSerializer
from notifications.models import Notifications


# Create your views here.
class NotificationsViewSet(ListModelMixin, GenericViewSet):
    serializer_class = NotificationsSerializer
    permission_classes = [IsAdminSuperUser]

    def get_queryset(self):
        user = self.request.user
        return Notifications.objects.filter(user=user).order_by('-create_at')
