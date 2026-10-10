from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsAuthority
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
        qs = self.get_queryset().filter(
            trips__status__in=["active", "paused"]
        ).distinct()
        serializer = self.get_serializer(qs, many=True)
        return Response({"success": True, "data": serializer.data})