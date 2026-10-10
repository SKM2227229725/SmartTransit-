from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BusViewSet

app_name = "buses"

router = DefaultRouter()
router.register("", BusViewSet, basename="bus")

urlpatterns = [
    path("", include(router.urls)),
]