from django.db.models import QuerySet
from rest_framework import generics, permissions

from apps.grades.api.serializers import StudentGradeSnapshotSerializer
from apps.grades.models import StudentGradeSnapshot
from apps.grades.selectors import get_student_grade_snapshots


class StudentGradeSnapshotDetailView(
    generics.RetrieveUpdateAPIView[StudentGradeSnapshot]
):
    permission_classes = [permissions.AllowAny]
    serializer_class = StudentGradeSnapshotSerializer
    queryset: QuerySet[StudentGradeSnapshot] = get_student_grade_snapshots()
    lookup_field = "uuid"
