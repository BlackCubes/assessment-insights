from collections.abc import Mapping
from typing import Any

from rest_framework.settings import api_settings

from .types import ErrorItem


def normalize_error_details(
    detail: Any, *, field: str | None = None
) -> list[ErrorItem]:
    """Recursively normalize error details into a list of ErrorItem dictionaries.

    Args:
        detail (Any): The error detail to normalize. It can be a string, list,
            tuple, or mapping (dictionary).
        field (str | None): The field name associated with the error detail. This is
            used to construct the "field" key in the resulting ErrorItem dictionaries.

    Returns:
        list[ErrorItem]: A list of normalized ErrorItem dictionaries, each containing
            "message", "code", and optionally "field" keys.

    Raises:
        TypeError: If the provided detail is not a string, list, tuple, or mapping.

    Note:
        - If the detail is a mapping with a single key "detail", it will be recursively
          normalized.
        - If the detail is a mapping with multiple keys, each key-value pair will be
          normalized, and the field name will be constructed based on the key.
        - If the detail is a list or tuple, each item will be normalized, and the
          field name will be constructed based on the index of the item.
        - If the detail is a string, it will be converted into an ErrorItem with the
          provided field name (if any) and a default error code of "error".

    Example:
        >>> normalize_error_details("An error occurred")
        [{'message': 'An error occurred', 'code': 'error'}]

        >>> normalize_error_details({"field1": "Error 1", "field2": "Error 2"})
        [
            {'message': 'Error 1', 'code': 'error', 'field': 'field1'},
            {'message': 'Error 2', 'code': 'error', 'field': 'field2'}
        ]

        >>> normalize_error_details(["Error 1", "Error 2"])
        [
            {'message': 'Error 1', 'code': 'error'},
            {'message': 'Error 2', 'code': 'error'}
        ]
    """
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
