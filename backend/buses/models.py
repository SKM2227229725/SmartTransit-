from django.core.validators import MinValueValidator
from django.db import models


class Bus(models.Model):
    """
    A physical bus in the fleet.
    GPS hardware is not deployed — the driver app simulates GPS.
    """

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        MAINTENANCE = "maintenance", "Maintenance"
        INACTIVE = "inactive", "Inactive"

    bus_number = models.CharField(
        max_length=20, unique=True, db_index=True,
        help_text="Public-facing bus number (e.g. MH13-001).",
    )
    license_plate = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField(
        default=40,
        validators=[MinValueValidator(1)],
    )
    model_name = models.CharField(max_length=80, blank=True)
    manufacture_year = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE, db_index=True
    )
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "buses_bus"
        ordering = ["bus_number"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["bus_number"]),
        ]
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"{self.bus_number} ({self.license_plate})"