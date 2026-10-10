from rest_framework import serializers

from .models import Bus


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = (
            "id", "bus_number", "license_plate", "capacity",
            "model_name", "manufacture_year", "status", "notes",
            "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_bus_number(self, value):
        value = value.strip()
        qs = Bus.objects.filter(bus_number__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Bus number already exists.")
        return value

    def validate_capacity(self, value):
        if value < 1:
            raise serializers.ValidationError("Capacity must be at least 1.")
        return value