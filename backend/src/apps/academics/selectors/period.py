from django.db.models import QuerySet
from apps.academics.models import Period

def get_periods() -> QuerySet[Period]:
  return Period.objects.all().order_by("period_number")
