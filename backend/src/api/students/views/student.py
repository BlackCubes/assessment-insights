from rest_framework import generics, permissions

from api.students.serializers import StudentSerializer
from apps.students.models import Student
from common.mixins import MultipleFieldLookupMixin


class StudentListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Student.objects.all().order_by("full_name")
    serializer_class = StudentSerializer


class StudentDetailView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Student.objects.all()
    lookup_fields = ["uuid", "student_id"]
