from django.contrib import admin

from .models import Fare


@admin.register(Fare)
class FareAdmin(admin.ModelAdmin):
    list_display = (
        "route", "origin_stop", "destination_stop",
        "distance_km", "amount",
    )
    list_filter = ("route",)
    search_fields = ("origin_stop__name", "destination_stop__name")
    autocomplete_fields = ("route", "origin_stop", "destination_stop")