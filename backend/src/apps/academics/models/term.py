from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel


class Term(BaseModel):
    class SemesterTypes(models.IntegerChoices):
        First = 1, _("First")
        Second = 2, _("Second")

    school_year = models.CharField(max_length=20)
    semester = models.PositiveIntegerField(
        choices=SemesterTypes,
        default=SemesterTypes.First,
        validators=[
            validators.MinValueValidator(limit_value=1),
            validators.MaxValueValidator(limit_value=2),
        ],
    )
    name = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["school_year", "semester"], name="unique_term"
            )
        ]

    def __str__(self):
        return f"{self.school_year} — {self.semester}"
