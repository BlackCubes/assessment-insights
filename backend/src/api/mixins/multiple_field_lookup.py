from collections.abc import Mapping, Sequence
from typing import Any, Generic, Protocol, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from rest_framework.exceptions import NotFound
from rest_framework.request import Request

from common.models import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)


class MultipleLookupView(Protocol[ModelT]):
    """
    Defines what a view must provide to use
    MultipleFieldLookupMixin.
    """

    @property
    def lookup_fields(self) -> Sequence[str]: ...

    @property
    def kwargs(self) -> Mapping[str, Any]: ...

    @property
    def request(self) -> Request: ...

    def get_queryset(self) -> QuerySet[ModelT]: ...

    def filter_queryset(
        self,
        queryset: QuerySet[ModelT],
    ) -> QuerySet[ModelT]: ...

    def check_object_permissions(
        self,
        request: Request,
        obj: ModelT,
    ) -> None: ...


class MultipleFieldLookupMixin(Generic[ModelT]):
    def get_object(
        self: MultipleLookupView[ModelT],
    ) -> ModelT:
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)

        lookup: dict[str, Any] = {}

        for field in self.lookup_fields:
            if field in self.kwargs:
                lookup[field] = self.kwargs[field]

        try:
            obj = queryset.get(**lookup)
        except ObjectDoesNotExist:
            model_name = queryset.model.__name__

            raise NotFound(f"The {model_name.lower()} does not exist.")

        self.check_object_permissions(self.request, obj)

        return obj
