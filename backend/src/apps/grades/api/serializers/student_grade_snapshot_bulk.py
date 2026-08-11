from typing import Any

from rest_framework import serializers

from apps.grades.api.serializers.student_grade_snapshot import (
    StudentGradeSnapshotSerializer,
)


class StudentGradeSnapshotBulkCreateSerializer(serializers.Serializer):
    snapshots = StudentGradeSnapshotSerializer(many=True)

    def validate_snapshots(self, value: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not value:
            raise serializers.ValidationError(
                "At least one snapshot is required.", code="empty"
            )

        return value
