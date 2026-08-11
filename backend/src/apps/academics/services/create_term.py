from dataclasses import dataclass

from django.db import IntegrityError, transaction

from apps.academics.exceptions import TermAlreadyExistsException
from apps.academics.models import Term


@dataclass(frozen=True, slots=True)
class CreateTermData:
    name: str
    school_year: str
    semester: int


def create_term(*, data: CreateTermData) -> Term:
    try:
        with transaction.atomic():
            return Term.objects.create(
                name=data.name.strip(),
                school_year=data.school_year.strip(),
                semester=data.semester,
            )
    except IntegrityError as exc:
        raise TermAlreadyExistsException("The term already exists.") from exc
