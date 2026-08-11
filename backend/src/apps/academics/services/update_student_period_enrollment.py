from dataclasses import dataclass

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.academics.exceptions import StudentPeriodEnrollmentAlreadyExistsException
from apps.academics.models import Period, StudentPeriodEnrollment, Term
from apps.students.models import Student


@dataclass(frozen=True, slots=True)
class UpdateStudentPeriodEnrollmentData:
    student: Student | None = None
    period: Period | None = None
    term: Term | None = None
    is_current: bool | None = None


def update_student_period_enrollment(
    *,
    student_period_enrollment: StudentPeriodEnrollment,
    data: UpdateStudentPeriodEnrollmentData,
) -> StudentPeriodEnrollment:
    updated_fields: list[str] = []

    if data.student is not None and student_period_enrollment.student != data.student:
        student_period_enrollment.student = data.student
        updated_fields.append("student")

    if data.period is not None and student_period_enrollment.period != data.period:
        student_period_enrollment.period = data.period
        updated_fields.append("period")

    if data.term is not None and student_period_enrollment.term != data.term:
        student_period_enrollment.term = data.term
        updated_fields.append("term")

    if (
        data.is_current is not None
        and student_period_enrollment.is_current != data.is_current
    ):
        student_period_enrollment.is_current = data.is_current
        updated_fields.append("is_current")

    if not updated_fields:
        return student_period_enrollment

    student_period_enrollment.updated_at = timezone.now()
    updated_fields.append("updated_at")

    try:
        with transaction.atomic():
            if student_period_enrollment.is_current:
                StudentPeriodEnrollment.objects.filter(
                    student=student_period_enrollment.student,
                    term=student_period_enrollment.term,
                    is_current=True,
                ).exclude(pk=student_period_enrollment.pk).update(
                    is_current=False, updated_at=timezone.now()
                )

            student_period_enrollment.save(update_fields=updated_fields)
    except IntegrityError as exc:
        raise StudentPeriodEnrollmentAlreadyExistsException(
            "The student period enrollment already exists."
        ) from exc

    return student_period_enrollment
