from django.contrib.auth import get_user_model
from rest_framework import serializers

from buses.models import Bus
from buses.serializers import BusSerializer
from routes.models import Route
from routes.serializers import RouteSerializer
from .models import PassengerCount, Trip

User = get_user_model()


class PassengerCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerCount
        fields = (
            "id", "trip", "stop", "count",
            "boarded", "alighted", "recorded_at",
        )
        read_only_fields = ("id", "recorded_at")


class TripSerializer(serializers.ModelSerializer):
    bus = BusSerializer(read_only=True)
    route = RouteSerializer(read_only=True)
    driver_email = serializers.CharField(source="driver.email", read_only=True)

    bus_id = serializers.PrimaryKeyRelatedField(
        queryset=Bus.objects.all(), source="bus", write_only=True
    )
    route_id = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.all(), source="route", write_only=True
    )
    driver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="driver"),
        source="driver", write_only=True, required=False,
    )

    class Meta:
        model = Trip
        fields = (
            "id", "bus", "bus_id", "route", "route_id",
            "driver", "driver_id", "driver_email",
            "status", "started_at", "ended_at", "scheduled_end_at",
            "total_passengers", "distance_covered_km", "notes",
            "created_at", "updated_at",
        )
        read_only_fields = (
            "id", "driver", "started_at", "ended_at",
            "created_at", "updated_at",
        )


class TripStartSerializer(serializers.Serializer):
    bus_id = serializers.IntegerField()
    route_id = serializers.IntegerField()

    def validate_bus_id(self, value):
        if not Bus.objects.filter(id=value, status="active").exists():
            raise serializers.ValidationError("Active bus with this id does not exist.")
        return value

    def validate_route_id(self, value):
        if not Route.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Active route with this id does not exist.")
        return value