from django.db.models import QuerySet

from apps.academics.models import Term


def get_terms() -> QuerySet[Term]:
    return Term.objects.all().order_by("school_year")
