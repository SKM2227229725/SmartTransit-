from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from buses.models import Bus
from routes.models import Route, Stop


class Trip(models.Model):
    """
    One run of a Bus on a Route, driven by a User with role='driver'.
    Only ONE trip may be active per driver at any time.
    """

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        PAUSED = "paused", "Paused"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    bus = models.ForeignKey(
        Bus, on_delete=models.PROTECT, related_name="trips"
    )
    route = models.ForeignKey(
        Route, on_delete=models.PROTECT, related_name="trips"
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="trips",
        limit_choices_to={"role": "driver"},
    )

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE,
        db_index=True,
    )
    started_at = models.DateTimeField(auto_now_add=True, db_index=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    scheduled_end_at = models.DateTimeField(null=True, blank=True)

    total_passengers = models.PositiveIntegerField(default=0)
    distance_covered_km = models.FloatField(default=0.0)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "trips_trip"
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["bus", "status"]),
            models.Index(fields=["driver", "status"]),
            models.Index(fields=["route", "status"]),
            models.Index(fields=["started_at"]),
        ]

    def __str__(self):
        return f"Trip #{self.pk} — {self.bus.bus_number} on {self.route.route_code}"


class PassengerCount(models.Model):
    """
    Passenger count snapshot for a Trip at a specific Stop.
    Used for demand forecasting (Prophet).
    """

    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="passenger_counts"
    )
    stop = models.ForeignKey(
        Stop, on_delete=models.PROTECT, related_name="passenger_counts"
    )
    count = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)]
    )
    boarded = models.PositiveIntegerField(default=0)
    alighted = models.PositiveIntegerField(default=0)

    recorded_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "trips_passenger_count"
        ordering = ["-recorded_at"]
        indexes = [
            models.Index(fields=["trip", "recorded_at"]),
            models.Index(fields=["stop", "recorded_at"]),
        ]

    def __str__(self):
        return f"Trip #{self.trip_id} @ {self.stop.name}: {self.count}"