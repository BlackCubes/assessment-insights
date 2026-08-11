from .base import AcademicsException


class TermException(AcademicsException):
    pass


class TermAlreadyExistsException(TermException):
    pass
