from typing import Literal, TypedDict

from typing_extensions import NotRequired


class ErrorItem(TypedDict):
    code: str
    field: NotRequired[str]
    message: str


class ErrorResponseData(TypedDict):
    errors: list[ErrorItem]
    message: str
    status: Literal["error"]
    statusCode: int
