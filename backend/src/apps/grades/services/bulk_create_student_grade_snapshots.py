from dataclasses import dataclass

from apps.grades.exceptions import StudentGradeSnapshotException
from apps.grades.models import StudentGradeSnapshot
from apps.grades.services.create_student_grade_snapshot import CreateStudentGradeSnapshotData, create_student_grade_snapshot


@dataclass(frozen=True, slots=True)
class BulkCreateResult:
    index: int
    snapshot: StudentGradeSnapshot | None
    error: str | None


def bulk_create_student_grade_snapshots(*, data: list[CreateStudentGradeSnapshotData]) -> list[BulkCreateResult]:
    results: list[BulkCreateResult] = []

    for index, item in enumerate(data):
        try:
            snapshot = create_student_grade_snapshot(data=item)

            results.append(BulkCreateResult(index=index, snapshot=snapshot, error=None))
        except StudentGradeSnapshotException as exc:
            results.append(BulkCreateResult(index=index, snapshot=None, error=str(exc)))

    return results
