from .utils import notificaion_unique_file_path
from django.db import models
from django.contrib.auth import get_user_model



# Create your models here.

class Device(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=False, null=True)
    token = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=False, null=True)
    title = models.CharField(max_length=254, blank=False, null=False)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to=notificaion_unique_file_path, blank=True, null=True)
    icon = models.FileField(upload_to=notificaion_unique_file_path, blank=True, null=True)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = 'User Notification'
        verbose_name_plural = 'User Notifications'
