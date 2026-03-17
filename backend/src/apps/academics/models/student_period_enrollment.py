from django.db import models

from common.models import BaseModel
from .period import Period
from .term import Term
from apps.students.models import Student

class StudentPeriodEnrollment(BaseModel):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="period_enrollments"
    )
    period = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name="student_enrollments"
    )
    term = models.ForeignKey(
        Term, on_delete=models.CASCADE, related_name="student_period_enrollments"
    )
    is_current = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "period", "term"], name="unique_student_period_term"
            ),
            models.UniqueConstraint(
                fields=["student", "term"],
                condition=models.Q(is_current=True),
                name="unique_current_period_per_student_per_term",
            ),
]
    def __str__(self):
        return f"{self.student} - {self.period} - {self.term}"