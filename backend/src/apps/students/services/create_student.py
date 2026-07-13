from dataclasses import dataclass

from django.db import IntegrityError, transaction

from apps.students.exceptions import StudentAlreadyExistException
from apps.students.models import Student


@dataclass(frozen=True, slots=True)
class CreateStudentData:
    full_name: str
    gender: str
    student_id: str


def create_student(*, data: CreateStudentData) -> Student:
    try:
        with transaction.atomic():
            return Student.objects.create(
                full_name=data.full_name.strip(),
                gender=data.gender.strip(),
                student_id=data.student_id.strip().upper(),
            )
    except IntegrityError as exc:
        raise StudentAlreadyExistException("The student already exists.") from exc
