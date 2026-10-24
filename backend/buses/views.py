from django.db.models import OuterRef, Subquery
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsAuthority
from tracking.models import LocationLog
from trips.models import Trip
from .models import Bus
from .serializers import BusSerializer


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["bus_number", "license_plate", "model_name"]
    ordering_fields = ["bus_number", "capacity", "created_at"]
    ordering = ["bus_number"]

    def get_permissions(self):
        if self.action in ("list", "retrieve", "active"):
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAuthority()]

    @action(detail=False, methods=["get"], url_path="active")
    def active(self, request):
        """
        GET /api/buses/active/
        Returns buses that have an active trip, along with their latest GPS location.
        """
        # Get latest location for each bus
        latest_location = LocationLog.objects.filter(bus=OuterRef('pk')).order_by('-timestamp')

        # Get buses that have active trips
        active_trips = Trip.objects.filter(status__in=["active", "paused"]).select_related("bus", "route")
        
        results = []
        for trip in active_trips:
            bus = trip.bus
            # Fetch the latest location log for this bus
            log = LocationLog.objects.filter(bus=bus).order_by("-timestamp").first()
            
            bus_data = {
                "bus_id": bus.id,
                "id": bus.id,  # Fallback for frontend
                "bus_number": bus.bus_number,
                "route_code": trip.route.route_code if trip.route else "N/A",
                "status": "active",
                "trip_id": trip.id,
                "latitude": log.latitude if log else None,
                "longitude": log.longitude if log else None,
                "speed": log.speed if log else 0.0,
                "timestamp": log.timestamp if log else None,
            }
            results.append(bus_data)
            
        return Response({"success": True, "data": results})