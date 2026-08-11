from .base import AcademicsException


class StudentPeriodEnrollmentException(AcademicsException):
    pass


class StudentPeriodEnrollmentAlreadyExistsException(StudentPeriodEnrollmentException):
    pass
