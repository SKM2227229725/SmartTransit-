from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from buses.models import Bus
from .models import LocationLog
from .serializers import LocationLogSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def bus_location(request, bus_id: int):
    bus = get_object_or_404(Bus, id=bus_id)
    latest = (
        LocationLog.objects.filter(bus=bus).order_by("-timestamp").first()
    )
    if not latest:
        return Response(
            {"success": True, "message": "No location data yet.", "data": None},
            status=status.HTTP_200_OK,
        )
    return Response({"success": True, "data": LocationLogSerializer(latest).data})