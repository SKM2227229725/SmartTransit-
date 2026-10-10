from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RouteViewSet, StopViewSet

app_name = "routes"

router = DefaultRouter()
router.register("routes", RouteViewSet, basename="route")
router.register("stops", StopViewSet, basename="stop")

urlpatterns = [
    path("", include(router.urls)),
]