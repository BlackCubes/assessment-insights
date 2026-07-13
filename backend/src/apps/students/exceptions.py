class StudentServiceException(Exception):
    pass


class StudentAlreadyExistException(StudentServiceException):
    pass
