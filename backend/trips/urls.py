from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TripViewSet

app_name = "trips"

router = DefaultRouter()
router.register("", TripViewSet, basename="trip")

urlpatterns = [
    path("", include(router.urls)),
]