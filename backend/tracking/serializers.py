from rest_framework import serializers

from .models import LocationLog


class LocationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationLog
        fields = (
            "id", "trip", "bus", "latitude", "longitude",
            "speed", "heading", "accuracy_meters", "timestamp", "source",
        )
        read_only_fields = ("id", "timestamp")