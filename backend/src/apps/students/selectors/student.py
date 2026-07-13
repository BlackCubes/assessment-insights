from django.db.models import QuerySet
from apps.students.models import Student

def get_students() -> QuerySet[Student]:
  return Student.objects.all().order_by("full_name")
