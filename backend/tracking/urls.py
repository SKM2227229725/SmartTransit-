from django.urls import path
from .views import bus_location, update_location

app_name = "tracking"

urlpatterns = [
    path("buses/<int:bus_id>/location/", bus_location, name="bus-location"),
    path("location/update/", update_location, name="update-location"),
    
]