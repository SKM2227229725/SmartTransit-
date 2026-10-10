from django.db import models

from routes.models import Route, Stop
from trips.models import Trip


class Fare(models.Model):
    """
    A computed fare for a segment of a route (origin → destination).
    Formula: base_fare + (distance_km * per_km_rate).
    """

    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="fares"
    )
    origin_stop = models.ForeignKey(
        Stop, on_delete=models.PROTECT, related_name="fares_from"
    )
    destination_stop = models.ForeignKey(
        Stop, on_delete=models.PROTECT, related_name="fares_to"
    )
    distance_km = models.FloatField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fares_fare"
        ordering = ["route", "origin_stop", "destination_stop"]
        constraints = [
            models.UniqueConstraint(
                fields=["route", "origin_stop", "destination_stop"],
                name="uniq_fare_segment_per_route",
            ),
        ]
        indexes = [
            models.Index(fields=["route"]),
            models.Index(fields=["origin_stop", "destination_stop"]),
        ]

    def __str__(self):
        return f"{self.route.route_code}: {self.origin_stop.name} → {self.destination_stop.name} = ₹{self.amount}"