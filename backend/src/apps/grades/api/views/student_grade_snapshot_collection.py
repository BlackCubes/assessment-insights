from django.db.models import QuerySet
from rest_framework import generics, permissions

from apps.grades.api.serializers import StudentGradeSnapshotSerializer
from apps.grades.models import StudentGradeSnapshot
from apps.grades.selectors import get_student_grade_snapshots


class StudentGradeSnapshotListCreateView(
    generics.ListCreateAPIView[StudentGradeSnapshot]
):
    permission_classes = [permissions.AllowAny]
    serializer_class = StudentGradeSnapshotSerializer
    queryset: QuerySet[StudentGradeSnapshot] = get_student_grade_snapshots()
