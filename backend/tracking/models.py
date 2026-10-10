from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from buses.models import Bus
from trips.models import Trip


class LocationLog(models.Model):
    """
    A single GPS ping from a driver's device.
    Expected frequency: every ~5 seconds while a trip is active.
    """

    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="location_logs"
    )
    bus = models.ForeignKey(
        Bus, on_delete=models.CASCADE, related_name="location_logs"
    )

    latitude = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)]
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)]
    )
    speed = models.FloatField(
        default=0.0, help_text="Instantaneous speed in km/h."
    )
    heading = models.FloatField(
        default=0.0, help_text="Direction of travel in degrees (0-360)."
    )
    accuracy_meters = models.FloatField(default=5.0)

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    source = models.CharField(
        max_length=20, default="simulator",
        help_text="'simulator' for driver app, 'device' for real GPS hardware later.",
    )

    class Meta:
        db_table = "tracking_location_log"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["trip", "-timestamp"]),
            models.Index(fields=["bus", "-timestamp"]),
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"Trip #{self.trip_id} @ {self.latitude:.4f},{self.longitude:.4f}"


class Anomaly(models.Model):
    """
    Anomaly detected by the Isolation Forest model or rule-based checks.
    Types: abnormal_speed, unusual_stoppage, route_deviation,
           long_inactivity, unusual_movement.
    """

    class AnomalyType(models.TextChoices):
        ABNORMAL_SPEED = "abnormal_speed", "Abnormal Speed"
        UNUSUAL_STOPPAGE = "unusual_stoppage", "Unusual Stoppage"
        ROUTE_DEVIATION = "route_deviation", "Route Deviation"
        LONG_INACTIVITY = "long_inactivity", "Long Inactivity"
        UNUSUAL_MOVEMENT = "unusual_movement", "Unusual Movement"

    class Severity(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    bus = models.ForeignKey(
        Bus, on_delete=models.CASCADE, related_name="anomalies"
    )
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="anomalies",
        null=True, blank=True,
    )
    anomaly_type = models.CharField(
        max_length=30, choices=AnomalyType.choices, db_index=True
    )
    severity = models.CharField(
        max_length=10, choices=Severity.choices, default=Severity.MEDIUM,
        db_index=True,
    )
    description = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    detected_at = models.DateTimeField(auto_now_add=True, db_index=True)
    resolved = models.BooleanField(default=False, db_index=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="resolved_anomalies",
    )

    class Meta:
        db_table = "tracking_anomaly"
        ordering = ["-detected_at"]
        indexes = [
            models.Index(fields=["bus", "resolved"]),
            models.Index(fields=["trip"]),
            models.Index(fields=["-detected_at"]),
        ]

    def __str__(self):
        return f"{self.anomaly_type} on Bus {self.bus_id} ({self.severity})"