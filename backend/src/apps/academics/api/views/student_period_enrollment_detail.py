from django.db.models import QuerySet
from rest_framework import generics, permissions

from apps.academics.api.serializers import StudentPeriodEnrollmentSerializer
from apps.academics.models import StudentPeriodEnrollment
from apps.academics.selectors import get_student_period_enrollments


class StudentPeriodEnrollmentDetailView(
    generics.RetrieveUpdateAPIView[StudentPeriodEnrollment]
):
    permission_classes = [permissions.AllowAny]
    serializer_class = StudentPeriodEnrollmentSerializer
    queryset: QuerySet[StudentPeriodEnrollment] = get_student_period_enrollments()
    lookup_field = "uuid"
