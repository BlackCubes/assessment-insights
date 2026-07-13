from dataclasses import dataclass

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.students.exceptions import StudentAlreadyExists
from apps.students.models import Student


@dataclass(frozen=True, slots=True)
class UpdateStudentData:
    full_name: str | None = None
    gender: str | None = None
    student_id: str | None = None


def update_student(*, student: Student, data: UpdateStudentData) -> Student:
    updated_fields: list[str] = []

    if data.full_name is not None:
        full_name = data.full_name.strip()

        if student.full_name != full_name:
            student.full_name = full_name
            updated_fields.append("full_name")

    if data.gender is not None:
        gender = data.gender.strip()

        if student.gender != gender:
            student.gender = gender
            updated_fields.append("gender")

    if data.student_id is not None:
        student_id = data.student_id.strip().upper()

        if student.student_id != student_id:
            student.student_id = student_id
            updated_fields.append("student_id")

    if not updated_fields:
        return student

    student.updated_at = timezone.now()
    updated_fields.append("updated_at")

    try:
        with transaction.atomic():
            student.save(update_fields=updated_fields)
    except IntegrityError as exc:
        raise StudentAlreadyExists("The student already exists.") from exc

    return student
