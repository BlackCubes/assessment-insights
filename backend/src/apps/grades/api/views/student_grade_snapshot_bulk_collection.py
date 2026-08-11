from typing import Any, cast

from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.grades.api.serializers import (
    StudentGradeSnapshotBulkCreateSerializer,
    StudentGradeSnapshotSerializer,
)
from apps.grades.services import (
    CreateStudentGradeSnapshotData,
    bulk_create_student_grade_snapshots,
)


class StudentGradeSnapshotBulkCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request) -> Response:
        serializer = StudentGradeSnapshotBulkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = cast(dict[str, Any], serializer.validated_data)

        items = [
            CreateStudentGradeSnapshotData(
                enrollment=row["enrollment"],
                grade=row["grade"],
                is_current_grade=row["is_current_grade"],
                recorded_at=row.get("recorded_at"),
            )
            for row in validated_data["snapshots"]
        ]

        results = bulk_create_student_grade_snapshots(data=items)

        response_data = [
            {
                "index": result.index,
                "status": "created" if result.snapshot else "error",
                "snapshot": (
                    StudentGradeSnapshotSerializer(result.snapshot).data
                    if result.snapshot
                    else None
                ),
                "error": result.error,
            }
            for result in results
        ]

        overall_status = (
            status.HTTP_201_CREATED
            if all(r.snapshot for r in results)
            else status.HTTP_207_MULTI_STATUS
        )

        return Response(response_data, status=overall_status)
