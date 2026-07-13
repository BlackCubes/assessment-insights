from rest_framework import generics, permissions
from apps.students.api.serializers import StudentSerializer
from apps.students.models import Student
from apps.students.selectors import get_students
from django.db.models import QuerySet

class StudentListCreateView(generics.ListCreateAPIView[Student]):
  permission_classes = [permissions.AllowAny]
  serializer_class = StudentSerializer
  queryset: QuerySet[Student] = get_students()