from django.db.models import QuerySet
from rest_framework import generics, permissions

from api.mixins import MultipleFieldLookupMixin
from apps.students.api.serializers import StudentSerializer
from apps.students.models import Student
from apps.students.selectors import get_students


class StudentDetailView(
    MultipleFieldLookupMixin, generics.RetrieveUpdateAPIView[Student]
):
    permission_classes = [permissions.AllowAny]
    serializer_class = StudentSerializer
    queryset: QuerySet[Student] = get_students()
    lookup_fields = ["uuid", "student_id"]
