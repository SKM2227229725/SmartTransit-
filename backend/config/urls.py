from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health(_request):
    return JsonResponse({"success": True, "service": "smarttransit", "status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health, name="health"),
    path("api/auth/", include("users.urls")),
    path("api/buses/", include("buses.urls")),
    path("api/", include("routes.urls")),
    path("api/trips/", include("trips.urls")),
    path("api/", include("tracking.urls")),
    path("api/", include("tracking.urls")),  
]