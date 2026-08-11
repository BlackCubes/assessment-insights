from typing import Any

from rest_framework import serializers

from apps.academics.exceptions import StudentPeriodEnrollmentAlreadyExistsException
from apps.academics.models import Period, StudentPeriodEnrollment, Term
from apps.academics.services import (
    CreateStudentPeriodEnrollmentData,
    UpdateStudentPeriodEnrollmentData,
    create_student_period_enrollment,
    update_student_period_enrollment,
)
from apps.students.models import Student


class StudentPeriodEnrollmentSerializer(
    serializers.ModelSerializer[StudentPeriodEnrollment]
):
    student = serializers.SlugRelatedField(
        slug_field="uuid", queryset=Student.objects.all()
    )
    period = serializers.SlugRelatedField(
        slug_field="uuid", queryset=Period.objects.all()
    )
    term = serializers.SlugRelatedField(slug_field="uuid", queryset=Term.objects.all())
    is_current = serializers.BooleanField(default=True)

    class Meta:
        model = StudentPeriodEnrollment
        fields = [
            "uuid",
            "student",
            "period",
            "term",
            "is_current",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uuid", "created_at", "updated_at"]

    def create(self, validated_data: dict[str, Any]) -> StudentPeriodEnrollment:
        try:
            return create_student_period_enrollment(
                data=CreateStudentPeriodEnrollmentData(
                    student=validated_data["student"],
                    period=validated_data["period"],
                    term=validated_data["term"],
                    is_current=validated_data["is_current"],
                )
            )
        except StudentPeriodEnrollmentAlreadyExistsException as exc:
            raise serializers.ValidationError(
                str(exc), code="student_period_enrollment_already_exists"
            ) from exc

    def update(
        self, instance: StudentPeriodEnrollment, validated_data: dict[str, Any]
    ) -> StudentPeriodEnrollment:
        try:
            return update_student_period_enrollment(
                student_period_enrollment=instance,
                data=UpdateStudentPeriodEnrollmentData(
                    student=validated_data.get("student"),
                    period=validated_data.get("period"),
                    term=validated_data.get("term"),
                    is_current=validated_data.get("is_current"),
                ),
            )
        except StudentPeriodEnrollmentAlreadyExistsException as exc:
            raise serializers.ValidationError(
                str(exc), code="student_period_enrollment_already_exists"
            ) from exc
