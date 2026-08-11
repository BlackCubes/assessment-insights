from django.db import models

from apps.academics.models import StudentPeriodEnrollment
from common.models import BaseModel
from common.utils import current_datetime_utc


class StudentGradeSnapshot(BaseModel):
    enrollment = models.ForeignKey(
        StudentPeriodEnrollment,
        on_delete=models.CASCADE,
        related_name="grade_snapshots",
        default=None,
    )
    grade = models.DecimalField(max_digits=5, decimal_places=4)
    is_current_grade = models.BooleanField(default=False)
    recorded_at = models.DateTimeField(default=current_datetime_utc())

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=["enrollment"],
                condition=models.Q(is_current_grade=True),
                name="unique_current_grade_per_enrollment",
            )
        ]

    def __str__(self):
        return (
            f"{self.enrollment} - "
            f"{self.grade} ({'current' if self.is_current_grade else 'historical'})"
        )
