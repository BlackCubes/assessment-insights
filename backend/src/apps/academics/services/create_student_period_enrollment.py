from dataclasses import dataclass

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.academics.exceptions import StudentPeriodEnrollmentAlreadyExistsException
from apps.academics.models import Period, StudentPeriodEnrollment, Term
from apps.students.models import Student


@dataclass(frozen=True, slots=True)
class CreateStudentPeriodEnrollmentData:
    student: Student
    period: Period
    term: Term
    is_current: bool


def create_student_period_enrollment(
    *, data: CreateStudentPeriodEnrollmentData
) -> StudentPeriodEnrollment:
    try:
        with transaction.atomic():
            if data.is_current:
                StudentPeriodEnrollment.objects.filter(
                    student=data.student, term=data.term, is_current=True
                ).update(is_current=False, updated_at=timezone.now())

            return StudentPeriodEnrollment.objects.create(
                student=data.student,
                period=data.period,
                term=data.term,
                is_current=data.is_current,
            )

    except IntegrityError as exc:
        raise StudentPeriodEnrollmentAlreadyExistsException(
            "The student period enrollment already exists."
        ) from exc
