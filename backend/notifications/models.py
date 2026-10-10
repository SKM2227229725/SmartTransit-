from django.conf import settings
from django.db import models

from buses.models import Bus


class Notification(models.Model):
    """
    A user-facing notification (approaching bus, delay, deviation, etc.).
    """

    class Kind(models.TextChoices):
        APPROACHING = "approaching", "Bus Approaching"
        DELAYED = "delayed", "Bus Delayed"
        DEVIATION = "deviation", "Route Deviation"
        UNAVAILABLE = "unavailable", "Bus Unavailable"
        ANOMALY = "anomaly", "Anomaly Detected"
        GENERAL = "general", "General"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    kind = models.CharField(
        max_length=20, choices=Kind.choices, default=Kind.GENERAL, db_index=True
    )
    title = models.CharField(max_length=150)
    message = models.TextField()
    bus = models.ForeignKey(
        Bus, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="notifications",
    )
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "notifications_notification"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "is_read"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"[{self.kind}] {self.title} → {self.user_id}"