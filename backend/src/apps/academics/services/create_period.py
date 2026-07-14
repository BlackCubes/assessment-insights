from dataclasses import dataclass

from django.db import IntegrityError, transaction

from apps.academics.exceptions import PeriodAlreadyExistsException
from apps.academics.models import Period


@dataclass(frozen=True, slots=True)
class CreatePeriodData:
    name: str
    period: int


def create_period(*, data: CreatePeriodData) -> Period:
    try:
        with transaction.atomic():
            return Period.objects.create(period=data.period, name=data.name.strip())
    except IntegrityError as exc:
        raise PeriodAlreadyExistsException("The period already exists.") from exc
