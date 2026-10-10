from django.contrib import admin

from .models import PassengerCount, Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = (
        "id", "bus", "route", "driver", "status",
        "started_at", "ended_at", "total_passengers",
    )
    list_filter = ("status", "route")
    search_fields = ("bus__bus_number", "route__route_code", "driver__email")
    autocomplete_fields = ("bus", "route", "driver")
    readonly_fields = ("started_at", "created_at", "updated_at")
    ordering = ("-started_at",)


@admin.register(PassengerCount)
class PassengerCountAdmin(admin.ModelAdmin):
    list_display = ("trip", "stop", "count", "boarded", "alighted", "recorded_at")
    list_filter = ("stop",)
    search_fields = ("trip__id", "stop__name")
    autocomplete_fields = ("trip", "stop")
    ordering = ("-recorded_at",)