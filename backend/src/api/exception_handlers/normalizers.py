from collections.abc import Mapping
from typing import Any

from rest_framework.settings import api_settings

from .types import ErrorItem


def normalize_error_details(
    detail: Any, *, field: str | None = None
) -> list[ErrorItem]:
    if isinstance(detail, Mapping):
        if len(detail) == 1 and "detail" in detail:
            return normalize_error_details(detail["detail"], field=field)

        errors: list[ErrorItem] = []

        for key, value in detail.items():
            key_string = str(key)

            if key_string == api_settings.NON_FIELD_ERRORS_KEY:
                child_field = field
            else:
                child_field = _append_field(field, key_string)

            errors.extend(normalize_error_details(value, field=child_field))

        return errors

    if isinstance(detail, (list, tuple)):
        errors: list[ErrorItem] = []

        contains_nested_items = any(
            isinstance(item, (Mapping, list, tuple)) for item in detail
        )

        for index, item in enumerate(detail):
            child_field = field

            if contains_nested_items and isinstance(item, (Mapping, list, tuple)):
                child_field = _append_index(field, index)

            errors.extend(normalize_error_details(item, field=child_field))

        return errors

    error: ErrorItem = {
        "message": str(detail),
        "code": str(getattr(detail, "code", "error")),
    }

    if field is not None:
        error["field"] = field

    return [error]


def _append_field(parent: str | None, child: str) -> str:
    if parent is None:
        return child

    return f"{parent}.{child}"


def _append_index(parent: str | None, index: int) -> str:
    if parent is None:
        return f"[{index}]"

    return f"{parent}[{index}]"
