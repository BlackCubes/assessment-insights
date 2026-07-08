from collections.abc import Mapping, Sequence
from typing import Any, Protocol, TypeVar

from django.db.models import QuerySet
from rest_framework.exceptions import NotFound
from rest_framework.request import Request

from common.models import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)


class MultipleLookupView(Protocol[ModelT]):
    """"""

    lookup_fields: Sequence[str]
    kwargs: Mapping[str, Any]
    request: Request

    def get_queryset(self) -> QuerySet[ModelT]:
        """Return the queryset used to retrieve the object."""
        ...

    def filter_queryset(
        self,
        queryset: QuerySet[ModelT],
    ) -> QuerySet[ModelT]:
        """Apply the view's configured filters to the queryset."""
        ...

    def check_object_permissions(
        self,
        request: Request,
        obj: ModelT,
    ) -> None:
        """Check whether the current request can access the object."""
        ...


class MultipleFieldLookupMixin:
    lookup_fields: Sequence[str] = []

    def get_object(self: MultipleLookupView[ModelT]) -> ModelT:
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)

        filter = {}

        for field in self.lookup_fields:
            if self.kwargs.get(field):
                filter[field] = self.kwargs[field]

        try:
            obj = queryset.get(**filter)
        except queryset.model.DoesNotExist:
            model_name = queryset.model.__name__

            raise NotFound(f"The {model_name.lower()} does not exist.")

        self.check_object_permissions(self.request, obj)

        return obj
