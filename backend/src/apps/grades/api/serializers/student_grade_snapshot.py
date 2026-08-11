from decimal import Decimal
from typing import Any

from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from apps.academics.models import StudentPeriodEnrollment
from apps.grades.exceptions import StudentAlreadyHasCurrentGradeSnapshotException
from apps.grades.models import StudentGradeSnapshot
from apps.grades.services import (
    CreateStudentGradeSnapshotData,
    UpdateStudentGradeSnapshotData,
    create_student_grade_snapshot,
    update_student_grade_snapshot,
)


class StudentGradeSnapshotSerializer(serializers.ModelSerializer[StudentGradeSnapshot]):
    enrollment = serializers.SlugRelatedField(
        slug_field="uuid", queryset=StudentPeriodEnrollment.objects.all()
    )
    grade = serializers.DecimalField(
        max_digits=5,
        decimal_places=4,
        validators=[
            MinValueValidator(Decimal("0")),
            MaxValueValidator(Decimal("0.9999")),
        ],
    )
    is_current_grade = serializers.BooleanField(default=True)
    recorded_at = serializers.DateTimeField(required=False)

    class Meta:
        model = StudentGradeSnapshot
        fields = [
            "uuid",
            "enrollment",
            "grade",
            "is_current_grade",
            "recorded_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uuid", "created_at", "updated_at"]

    def create(self, validated_data: dict[str, Any]) -> StudentGradeSnapshot:
        try:
            return create_student_grade_snapshot(
                data=CreateStudentGradeSnapshotData(
                    enrollment=validated_data["enrollment"],
                    grade=validated_data["grade"],
                    is_current_grade=validated_data["is_current_grade"],
                    recorded_at=validated_data.get("recorded_at"),
                )
            )
        except StudentAlreadyHasCurrentGradeSnapshotException as exc:
            raise serializers.ValidationError(
                str(exc), code="student_already_has_current_grade_snapshot"
            ) from exc

    def update(
        self, instance: StudentGradeSnapshot, validated_data: dict[str, Any]
    ) -> StudentGradeSnapshot:
        try:
            return update_student_grade_snapshot(
                student_grade_snapshot=instance,
                data=UpdateStudentGradeSnapshotData(
                    grade=validated_data.get("grade"),
                    is_current_grade=validated_data.get("is_current_grade"),
                    recorded_at=validated_data.get("recorded_at"),
                ),
            )
        except StudentAlreadyHasCurrentGradeSnapshotException as exc:
            raise serializers.ValidationError(
                str(exc), code="student_already_has_current_grade_snapshot"
            ) from exc
