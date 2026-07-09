from rest_framework import status
from rest_framework.exceptions import APIException


class ServiceUnavailableException(APIException):
    default_code = "service_unavailable"
    default_detail = "The service is temporarily unavailable."
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
