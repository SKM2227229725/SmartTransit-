from django.urls import path

from .views import bus_location

app_name = "tracking"

urlpatterns = [
    path("buses/<int:bus_id>/location/", bus_location, name="bus-location"),
]