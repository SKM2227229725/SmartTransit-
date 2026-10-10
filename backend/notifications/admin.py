from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "kind", "title", "is_read", "created_at")
    list_filter = ("kind", "is_read")
    search_fields = ("user__email", "title", "message")
    autocomplete_fields = ("user", "bus")
    ordering = ("-created_at",)