from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsAuthority
from .models import Route, RouteStop, Stop
from .serializers import (
    RouteSerializer,
    RouteStopSerializer,
    RouteStopWriteSerializer,
    StopSerializer,
)


class StopViewSet(viewsets.ModelViewSet):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "landmark"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAuthority()]


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.prefetch_related("route_stops__stop").all()
    serializer_class = RouteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["route_code", "name"]
    ordering_fields = ["route_code", "name", "created_at"]
    ordering = ["route_code"]

    def get_permissions(self):
        if self.action in ("list", "retrieve", "stops"):
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAuthority()]

    @action(detail=True, methods=["get"], url_path="stops")
    def stops(self, request, pk=None):
        route = self.get_object()
        qs = route.route_stops.select_related("stop").order_by("sequence")
        serializer = RouteStopSerializer(qs, many=True)
        return Response({
            "success": True,
            "route": {"id": route.id, "route_code": route.route_code, "name": route.name},
            "data": serializer.data,
        })

    @action(detail=True, methods=["post"], url_path="set-stops")
    def set_stops(self, request, pk=None):
        route = self.get_object()
        if not (request.user.role == "authority" or request.user.is_superuser):
            return Response(
                {"success": False, "message": "Authority access required.", "errors": {}},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = RouteStopWriteSerializer(data=request.data.get("stops", []), many=True)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            route.route_stops.all().delete()
            objs = []
            for item in serializer.validated_data:
                stop = get_object_or_404(Stop, id=item["stop_id"])
                objs.append(RouteStop(route=route, stop=stop, **{
                    k: v for k, v in item.items() if k != "stop_id"
                }))
            RouteStop.objects.bulk_create(objs)

        qs = route.route_stops.select_related("stop").order_by("sequence")
        return Response({
            "success": True,
            "message": "Route stops updated.",
            "data": RouteStopSerializer(qs, many=True).data,
        })