from django.core.validators import MinValueValidator
from django.db import models


class Route(models.Model):
    """A named bus route with a base fare."""

    route_code = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    base_fare = models.DecimalField(
        max_digits=8, decimal_places=2, default=10.00,
        validators=[MinValueValidator(0)],
    )
    per_km_rate = models.DecimalField(
        max_digits=6, decimal_places=2, default=2.50,
        validators=[MinValueValidator(0)],
    )
    is_active = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "routes_route"
        ordering = ["route_code"]
        indexes = [
            models.Index(fields=["route_code"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.route_code} — {self.name}"


class Stop(models.Model):
    """A bus stop with geographic coordinates."""

    name = models.CharField(max_length=120, db_index=True)
    latitude = models.FloatField(db_index=True)
    longitude = models.FloatField(db_index=True)
    landmark = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "routes_stop"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "latitude", "longitude"],
                name="uniq_stop_name_location",
            ),
        ]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.latitude:.4f}, {self.longitude:.4f})"


class RouteStop(models.Model):
    """
    Through table: a Stop at a specific sequence on a Route.
    sequence=1 is the first stop, sequence=N is the last.
    """

    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="route_stops"
    )
    stop = models.ForeignKey(
        Stop, on_delete=models.CASCADE, related_name="route_stops"
    )
    sequence = models.PositiveIntegerField()
    distance_from_start_km = models.FloatField(
        default=0.0, help_text="Cumulative distance from route origin (km)."
    )
    scheduled_offset_minutes = models.PositiveIntegerField(
        default=0,
        help_text="Expected minutes from trip start to reach this stop.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "routes_route_stop"
        ordering = ["route", "sequence"]
        constraints = [
            models.UniqueConstraint(
                fields=["route", "sequence"],
                name="uniq_route_sequence",
            ),
            models.UniqueConstraint(
                fields=["route", "stop"],
                name="uniq_route_stop",
            ),
        ]
        indexes = [
            models.Index(fields=["route", "sequence"]),
            models.Index(fields=["stop"]),
        ]

    def __str__(self):
        return f"{self.route.route_code} #{self.sequence} — {self.stop.name}"