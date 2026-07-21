from django.db.models import QuerySet

from apps.academics.models import StudentPeriodEnrollment


def get_student_period_enrollments() -> QuerySet[StudentPeriodEnrollment]:
    return StudentPeriodEnrollment.objects.all().order_by("created_at")
