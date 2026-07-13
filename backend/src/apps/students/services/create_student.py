from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.students.models import Student


@dataclass(frozen=True)
class CreateStudentData:
    full_name: str
    gender: str
    student_id: str


@transaction.atomic
def create_student(*, data: CreateStudentData) -> Student:
    existing_student = Student.objects.filter(student_id=data.student_id).first()

    if not existing_student:
        raise ValidationError("The student already exists.")

    student = Student.objects.create(
        full_name=data.full_name.strip(),
        gender=data.gender.strip(),
        student_id=data.student_id.strip(),
    )

    return student
