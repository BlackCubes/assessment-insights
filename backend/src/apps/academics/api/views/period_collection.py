from django.db.models import QuerySet
from rest_framework import generics, permissions

from apps.academics.api.serializers import PeriodSerializer
from apps.academics.models import Period
from apps.academics.selectors import get_periods


class PeriodListCreateView(generics.ListCreateAPIView[Period]):
    permission_classes = [permissions.AllowAny]
    serializer_class = PeriodSerializer
    queryset: QuerySet[Period] = get_periods()
