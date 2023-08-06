from .models import Notification
from django.contrib import admin

# Register your models here.
@admin.register(Notification)
class NotificationView(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'is_read', 'created_at']
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    raw_id_fields = ('user',)
