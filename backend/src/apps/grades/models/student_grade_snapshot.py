from django.db import models

from apps.academics.models import Term
from apps.students.models import Student
from common.models import BaseModel
from common.utils import current_datetime_utc


class StudentGradeSnapshot(BaseModel):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="grade_snapshots"
    )
    term = models.ForeignKey(
        Term, on_delete=models.CASCADE, related_name="student_grade_snapshots"
    )
    grade = models.DecimalField(max_digits=5, decimal_places=4)
    is_current_grade = models.BooleanField(default=False)
    recorded_at = models.DateTimeField(default=current_datetime_utc())

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "term"],
                condition=models.Q(is_current_grade=True),
                name="unique_current_grade_per_student_term",
            )
        ]

    def __str__(self):
        return (
            f"{self.student} - {self.term} - "
            f"{self.grade} ({'current' if self.is_current_grade else 'historical'})"
        )
