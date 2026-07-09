import logging
from collections.abc import Mapping
from http import HTTPStatus
from typing import Any

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from .normalizers import normalize_error_details
from .types import ErrorItem, ErrorResponseData

logger = logging.getLogger(__name__)


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    response = drf_exception_handler(exc, context)

    if response is None:
        return _handle_unexpected_exception(exc=exc, context=context)

    response_data = response.data
    message = _get_error_message(
        exc=exc, response_data=response_data, status_code=response.status_code
    )

    errors: list[ErrorItem] = normalize_error_details(response_data)

    if not errors:
        errors.append({"message": message, "code": "error"})

    payload: ErrorResponseData = {
        "errors": errors,
        "message": message,
        "status": "error",
        "statusCode": response.status_code,
    }

    response.data = payload

    return response


def _get_error_message(*, exc: Exception, response_data: Any, status_code: int) -> str:
    if isinstance(exc, ValidationError):
        return "Validation failed."

    if isinstance(response_data, Mapping):
        detail = response_data.get("detail")

        if detail is not None and not isinstance(detail, (Mapping, list, tuple)):
            return str(detail)

    return _get_default_status_message(status_code)


def _get_default_status_message(status_code: int) -> str:
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return "The request could not be completed."


def _handle_unexpected_exception(
    *, exc: Exception, context: dict[str, Any]
) -> Response:
    request = context.get("request")
    view = context.get("view")

    view_name: str | None = None

    if view is not None:
        view_class = view.__class__
        view_name = f"{view_class.__module__}." f"{view_class.__qualname__}"

    logger.error(
        "Unhandled exception raised by API view.",
        extra={
            "request_method": getattr(request, "method", None),
            "request_path": getattr(request, "path", None),
            "view_name": view_name,
        },
        exc_info=(type(exc), exc, exc.__traceback__),
    )

    message = "An unexpected server error occurred."

    payload: ErrorResponseData = {
        "errors": [{"message": message, "code": "server_error"}],
        "message": message,
        "status": "error",
        "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
    }

    return Response(data=payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
