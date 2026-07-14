from django.db.models import QuerySet
from rest_framework import generics, permissions

from api.mixins import MultipleFieldLookupMixin
from apps.academics.api.serializers import PeriodSerializer
from apps.academics.models import Period
from apps.academics.selectors import get_periods


class PeriodDetailView(
    MultipleFieldLookupMixin, generics.RetrieveUpdateAPIView[Period]
):
    permission_classes = [permissions.AllowAny]
    serializer_class = PeriodSerializer
    queryset: QuerySet[Period] = get_periods()
    lookup_fields = ["uuid", "period_number"]
