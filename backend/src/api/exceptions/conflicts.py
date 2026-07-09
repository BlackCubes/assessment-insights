from rest_framework import status
from rest_framework.exceptions import APIException


class ConflictException(APIException):
    default_code = "conflict"
    default_detail = "The request conflicts with the current resource state."
    status_code = status.HTTP_409_CONFLICT
