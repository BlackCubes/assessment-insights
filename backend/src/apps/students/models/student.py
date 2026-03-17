from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel


class Student(BaseModel):
    class GenderTypes(models.TextChoices):
        Male = "M", _("Male")
        Female = "F", _("Female")
        Other = "O", _("Other")

    student_id = models.CharField(unique=True, max_length=10)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=2, choices=GenderTypes)
