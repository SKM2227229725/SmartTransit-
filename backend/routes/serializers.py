from rest_framework import serializers

from .models import Route, RouteStop, Stop


class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = (
            "id", "name", "latitude", "longitude", "landmark",
            "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class RouteStopSerializer(serializers.ModelSerializer):
    stop = StopSerializer(read_only=True)
    stop_id = serializers.PrimaryKeyRelatedField(
        queryset=Stop.objects.all(), source="stop", write_only=True
    )

    class Meta:
        model = RouteStop
        fields = (
            "id", "stop", "stop_id", "sequence",
            "distance_from_start_km", "scheduled_offset_minutes",
        )
        read_only_fields = ("id",)


class RouteSerializer(serializers.ModelSerializer):
    route_stops = RouteStopSerializer(many=True, read_only=True)
    stop_count = serializers.IntegerField(source="route_stops.count", read_only=True)

    class Meta:
        model = Route
        fields = (
            "id", "route_code", "name", "description",
            "base_fare", "per_km_rate", "is_active",
            "route_stops", "stop_count",
            "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_route_code(self, value):
        value = value.strip()
        qs = Route.objects.filter(route_code__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Route code already exists.")
        return value


class RouteStopWriteSerializer(serializers.Serializer):
    stop_id = serializers.IntegerField()
    sequence = serializers.IntegerField(min_value=1)
    distance_from_start_km = serializers.FloatField(min_value=0, default=0.0)
    scheduled_offset_minutes = serializers.IntegerField(min_value=0, default=0)