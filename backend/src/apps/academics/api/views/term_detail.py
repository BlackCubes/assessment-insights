from django.db.models import QuerySet
from rest_framework import generics, permissions

from api.mixins import MultipleFieldLookupMixin
from apps.academics.api.serializers import TermSerializer
from apps.academics.models import Term
from apps.academics.selectors import get_terms


class TermDetailView(MultipleFieldLookupMixin, generics.RetrieveUpdateAPIView[Term]):
    permission_classes = [permissions.AllowAny]
    serializer_class = TermSerializer
    queryset: QuerySet[Term] = get_terms()
    lookup_fields = ["uuid", "semester"]
