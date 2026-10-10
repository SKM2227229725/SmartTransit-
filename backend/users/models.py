from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user with role-based access.
    Roles: passenger, driver, authority
    """

    class Role(models.TextChoices):
        PASSENGER = "passenger", "Passenger"
        DRIVER = "driver", "Driver"
        AUTHORITY = "authority", "Authority"

    email = models.EmailField(unique=True, db_index=True)
    full_name = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.PASSENGER, db_index=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users_user"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["role"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def is_passenger(self) -> bool:
        return self.role == self.Role.PASSENGER

    @property
    def is_driver(self) -> bool:
        return self.role == self.Role.DRIVER

    @property
    def is_authority(self) -> bool:
        return self.role == self.Role.AUTHORITY