from django.core import validators
from django.db import models

from common.models import BaseModel


class Period(BaseModel):
    period_number = models.PositiveIntegerField(
        validators=[validators.MinValueValidator(limit_value=1)]
    )
    name = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "period_number"], name="unique_period"
            )
        ]

    def __str__(self):
        return self.name
