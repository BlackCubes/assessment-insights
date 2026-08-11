from .base import AcademicsException


class PeriodException(AcademicsException):
    pass


class PeriodAlreadyExistsException(PeriodException):
    pass
