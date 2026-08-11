from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.grades.exceptions import StudentAlreadyHasCurrentGradeSnapshotException
from apps.grades.models import StudentGradeSnapshot


@dataclass(frozen=True, slots=True)
class UpdateStudentGradeSnapshotData:
    grade: Decimal | None = None
    is_current_grade: bool | None = None
    recorded_at: datetime | None = None


def update_student_grade_snapshot(
    *,
    student_grade_snapshot: StudentGradeSnapshot,
    data: UpdateStudentGradeSnapshotData,
) -> StudentGradeSnapshot:
    updated_fields: list[str] = []

    if data.grade is not None and student_grade_snapshot.grade != data.grade:
        student_grade_snapshot.grade = data.grade
        updated_fields.append("grade")

    if (
        data.is_current_grade is not None
        and student_grade_snapshot.is_current_grade != data.is_current_grade
    ):
        student_grade_snapshot.is_current_grade = data.is_current_grade
        updated_fields.append("is_current_grade")

    if (
        data.recorded_at is not None
        and student_grade_snapshot.recorded_at != data.recorded_at
    ):
        student_grade_snapshot.recorded_at = data.recorded_at
        updated_fields.append("recorded_at")

    if not updated_fields:
        return student_grade_snapshot

    student_grade_snapshot.updated_at = timezone.now()
    updated_fields.append("updated_at")

    try:
        with transaction.atomic():
            if student_grade_snapshot.is_current_grade:
                StudentGradeSnapshot.objects.filter(
                    enrollment=student_grade_snapshot.enrollment,
                    is_current_grade=True,
                ).exclude(pk=student_grade_snapshot.pk).update(
                    is_current_grade=False, updated_at=timezone.now()
                )

            student_grade_snapshot.save(update_fields=updated_fields)
    except IntegrityError as exc:
        raise StudentAlreadyHasCurrentGradeSnapshotException(
            "The student already has a current grade snapshot for this enrollment."
        ) from exc

    return student_grade_snapshot
