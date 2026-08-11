from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.defaults import page_not_found

from api.exception_handlers.types import ErrorResponseData


def api_page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    if not request.path.startswith("/api/"):
        return page_not_found(request, exception)

    message = "The requested API endpoint was not found."

    payload: ErrorResponseData = {
        "errors": [{"code": "not_found", "message": message}],
        "message": message,
        "status": "error",
        "statusCode": 404,
    }

    return JsonResponse(data=payload, status=404)
