from dataclasses import dataclass

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.academics.exceptions import PeriodAlreadyExistsException
from apps.academics.models import Period


@dataclass(frozen=True, slots=True)
class UpdatePeriodData:
    name: str | None = None
    period_number: int | None = None


def update_period(*, period: Period, data: UpdatePeriodData) -> Period:
    updated_fields: list[str] = []

    if data.name is not None:
        name = data.name.strip()

        if period.name != name:
            period.name = name
            updated_fields.append("name")

    if data.period_number is not None:
        period_numer = data.period_number

        if period.period_number != period_numer:
            period.period_number = period_numer
            updated_fields.append("period_number")

    if not updated_fields:
        return period

    period.updated_at = timezone.now()
    updated_fields.append("updated_at")

    try:
        with transaction.atomic():
            period.save(update_fields=updated_fields)
    except IntegrityError as exc:
        raise PeriodAlreadyExistsException("The period already exists.") from exc

    return period
