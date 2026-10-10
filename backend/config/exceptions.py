"""
Central DRF exception handler.
Ensures every error response matches:
    { "success": false, "message": "...", "errors": {...} }
"""

from rest_framework.views import exception_handler


def smarttransit_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return None

    data = response.data
    message = "Request failed"
    errors = {}

    if isinstance(data, dict):
        if "detail" in data:
            message = str(data["detail"])
        else:
            errors = data
            message = "Validation error" if response.status_code == 400 else message
    elif isinstance(data, list):
        errors = {"non_field_errors": data}
        message = "Validation error"

    response.data = {
        "success": False,
        "message": message,
        "errors": errors,
    }
    return response