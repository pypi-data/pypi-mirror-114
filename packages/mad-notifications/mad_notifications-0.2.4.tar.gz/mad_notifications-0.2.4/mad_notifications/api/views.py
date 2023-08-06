from ..models import Device, Notification
from .serializers import NotificationSerializer
from django.shortcuts import render
from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response

# Create your views here.

class DeviceViewSet(viewsets.ModelViewSet):
    this_view = 'notifications'

    throttle_scope = this_view
    required_scopes = [this_view]

    queryset = Device.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer



class NotificationViewSet(
        viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
    ):
    """
    User Notifications API
    """
    this_view = 'notifications'

    throttle_scope = this_view
    required_scopes = [this_view]

    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_read == False:
            instance.is_read = True
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
