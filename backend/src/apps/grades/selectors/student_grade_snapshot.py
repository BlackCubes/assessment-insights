from django.db.models import QuerySet

from apps.grades.models import StudentGradeSnapshot


def get_student_grade_snapshots() -> QuerySet[StudentGradeSnapshot]:
    return StudentGradeSnapshot.objects.all().order_by("recorded_at")
