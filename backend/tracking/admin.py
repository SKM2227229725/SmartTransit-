from django.contrib import admin

from .models import Anomaly, LocationLog


@admin.register(LocationLog)
class LocationLogAdmin(admin.ModelAdmin):
    list_display = ("id", "trip", "bus", "latitude", "longitude", "speed", "timestamp")
    list_filter = ("source", "bus")
    search_fields = ("trip__id", "bus__bus_number")
    autocomplete_fields = ("trip", "bus")
    readonly_fields = ("timestamp",)
    ordering = ("-timestamp",)


@admin.register(Anomaly)
class AnomalyAdmin(admin.ModelAdmin):
    list_display = (
        "id", "anomaly_type", "bus", "trip", "severity",
        "resolved", "detected_at",
    )
    list_filter = ("anomaly_type", "severity", "resolved")
    search_fields = ("bus__bus_number", "description")
    autocomplete_fields = ("bus", "trip", "resolved_by")
    readonly_fields = ("detected_at",)
    ordering = ("-detected_at",)