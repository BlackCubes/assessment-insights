from .base import GradesException


class StudentGradeSnapshotException(GradesException):
    pass


class StudentAlreadyHasCurrentGradeSnapshotException(StudentGradeSnapshotException):
    pass
