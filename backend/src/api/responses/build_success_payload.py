from collections.abc import Mapping
from typing import Any


def build_success_payload(data: Any, status_code: int) -> dict[str, Any]:
    """
    Build a success payload for API responses.

    Args:
        data (Any): The data to include in the payload.
        status_code (int): The HTTP status code for the response.

    Returns:
        dict[str, Any]: A dictionary containing the success payload.
    """
    payload: dict[str, Any] = {
        "status": "success",
        "statusCode": status_code,
        "data": data,
    }

    if isinstance(data, Mapping) and "results" in data and "metaData" in data:
        payload["data"] = data["results"]
        payload["metaData"] = data["metaData"]

    return payload
