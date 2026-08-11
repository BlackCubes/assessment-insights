from dataclasses import dataclass

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.academics.exceptions import TermAlreadyExistsException
from apps.academics.models import Term


@dataclass(frozen=True, slots=True)
class UpdateTermData:
    name: str | None = None
    school_year: str | None = None
    semester: int | None = None


def update_term(*, term: Term, data: UpdateTermData) -> Term:
    updated_fields: list[str] = []

    if data.name is not None:
        name = data.name.strip()

        if term.name != name:
            term.name = name
            updated_fields.append("name")

    if data.school_year is not None:
        school_year = data.school_year.strip()

        if term.school_year != school_year:
            term.school_year = school_year
            updated_fields.append("school_year")

    if data.semester is not None:
        semester = data.semester

        if term.semester != semester:
            term.semester = semester
            updated_fields.append("semester")

    if not updated_fields:
        return term

    term.updated_at = timezone.now()
    updated_fields.append("updated_at")

    try:
        with transaction.atomic():
            term.save(update_fields=updated_fields)
    except IntegrityError as exc:
        raise TermAlreadyExistsException("The term already exists.") from exc

    return term
