from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.academics.models import StudentPeriodEnrollment
from apps.grades.exceptions import StudentAlreadyHasCurrentGradeSnapshotException
from apps.grades.models import StudentGradeSnapshot


@dataclass(frozen=True, slots=True)
class CreateStudentGradeSnapshotData:
    enrollment: StudentPeriodEnrollment
    grade: Decimal
    is_current_grade: bool
    recorded_at: datetime | None = None


def create_student_grade_snapshot(
    *, data: CreateStudentGradeSnapshotData
) -> StudentGradeSnapshot:
    try:
        with transaction.atomic():
            if data.is_current_grade:
                StudentGradeSnapshot.objects.filter(
                    enrollment=data.enrollment, is_current_grade=True
                ).update(is_current_grade=False, updated_at=timezone.now())

            return StudentGradeSnapshot.objects.create(
                enrollment=data.enrollment,
                grade=data.grade,
                is_current_grade=data.is_current_grade,
                recorded_at=data.recorded_at or timezone.now(),
            )
    except IntegrityError as exc:
        raise StudentAlreadyHasCurrentGradeSnapshotException(
            "The student already has a current grade snapshot for this enrollment."
        ) from exc
