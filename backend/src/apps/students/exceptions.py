class StudentServiceError(Exception):
    pass


class StudentAlreadyExists(StudentServiceError):
    pass
