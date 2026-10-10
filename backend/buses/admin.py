from django.contrib import admin

from .models import Bus


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("bus_number", "license_plate", "capacity", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("bus_number", "license_plate", "model_name")
    ordering = ("bus_number",)