from rest_framework import generics, permissions

from api.mixins import MultipleFieldLookupMixin
from api.students.serializers import StudentSerializer
from apps.students.models import Student


class StudentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Student.objects.all().order_by("full_name")
    serializer_class = StudentSerializer


class StudentDetailUpdateView(MultipleFieldLookupMixin, generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_fields = ["uuid", "student_id"]
