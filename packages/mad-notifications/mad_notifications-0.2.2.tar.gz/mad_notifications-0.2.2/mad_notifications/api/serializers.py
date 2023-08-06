from ..models import Device, Notification
from rest_framework import serializers



class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            'id',
            'user',
            'token',

            'created_at', 'updated_at',
            'url',
        )


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id',
            'user',
            'title',
            'content',
            'is_read',
            'icon',
            'image',

            'created_at', 'updated_at',
            'url',
        )
        read_only_fields = fields
