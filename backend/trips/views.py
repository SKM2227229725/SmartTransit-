from django.db import transaction
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from buses.models import Bus
from routes.models import Route
from users.permissions import IsAuthority, IsDriver
from .models import Trip
from .serializers import TripSerializer, TripStartSerializer


class TripViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Trip.objects.select_related("bus", "route", "driver")
        if user.role == "authority" or user.is_superuser:
            return qs
        if user.role == "driver":
            return qs.filter(driver=user)
        return qs.filter(status__in=["active", "paused"])

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated, IsDriver])
    def start(self, request):
        serializer = TripStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Trip.objects.filter(driver=request.user, status__in=["active", "paused"]).exists():
            return Response(
                {"success": False, "message": "You already have an active trip.", "errors": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bus = Bus.objects.get(id=serializer.validated_data["bus_id"])
        route = Route.objects.get(id=serializer.validated_data["route_id"])

        with transaction.atomic():
            trip = Trip.objects.create(
                bus=bus, route=route, driver=request.user, status="active"
            )

        return Response(
            {"success": True, "message": "Trip started.", "data": TripSerializer(trip).data},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def end(self, request, pk=None):
        trip = self.get_object()
        if not (request.user.role == "authority" or trip.driver == request.user):
            return Response(
                {"success": False, "message": "Not allowed to end this trip.", "errors": {}},
                status=status.HTTP_403_FORBIDDEN,
            )
        if trip.status in ("completed", "cancelled"):
            return Response(
                {"success": False, "message": "Trip already ended.", "errors": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        trip.status = "completed"
        trip.ended_at = timezone.now()
        trip.save(update_fields=["status", "ended_at", "updated_at"])
        return Response({"success": True, "message": "Trip ended.", "data": TripSerializer(trip).data})

    @action(detail=False, methods=["get"], url_path="active")
    def active(self, request):
        qs = Trip.objects.filter(status__in=["active", "paused"]).select_related(
            "bus", "route", "driver"
        )
        return Response({"success": True, "data": TripSerializer(qs, many=True).data})

    @action(detail=False, methods=["get"], url_path="my", permission_classes=[IsAuthenticated, IsDriver])
    def my(self, request):
        qs = Trip.objects.filter(driver=request.user).select_related("bus", "route")
        return Response({"success": True, "data": TripSerializer(qs, many=True).data})