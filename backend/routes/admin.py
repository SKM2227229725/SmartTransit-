from django.contrib import admin

from .models import Route, RouteStop, Stop


class RouteStopInline(admin.TabularInline):
    model = RouteStop
    extra = 1
    autocomplete_fields = ("stop",)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("route_code", "name", "base_fare", "per_km_rate", "is_active")
    list_filter = ("is_active",)
    search_fields = ("route_code", "name")
    inlines = [RouteStopInline]


@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude", "landmark")
    search_fields = ("name", "landmark")


@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ("route", "sequence", "stop", "distance_from_start_km")
    list_filter = ("route",)
    search_fields = ("stop__name", "route__route_code")
    ordering = ("route", "sequence")