from typing import Any

from rest_framework import serializers

from apps.students.exceptions import StudentAlreadyExistException
from apps.students.models import Student
from apps.students.services import (
    CreateStudentData,
    UpdateStudentData,
    create_student,
    update_student,
)


class StudentSerializer(serializers.ModelSerializer[Student]):
    full_name = serializers.CharField(max_length=255)
    gender = serializers.ChoiceField(choices=["M", "F", "O"])
    student_id = serializers.CharField(max_length=10)

    class Meta:
        model = Student
        fields = [
            "uuid",
            "student_id",
            "full_name",
            "gender",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uuid", "created_at", "updated_at"]

    def validate_student_id(self, value: str) -> str:
        student_id = value.strip().upper()

        queryset = Student.objects.filter(student_id__iexact=student_id)

        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "A student with this ID already exists.", code="unique"
            )

        return student_id

    def create(self, validated_data: dict[str, Any]) -> Student:
        try:
            return create_student(
                data=CreateStudentData(
                    full_name=validated_data["full_name"],
                    gender=validated_data["gender"],
                    student_id=validated_data["student_id"],
                )
            )
        except StudentAlreadyExistException as exc:
            raise serializers.ValidationError(
                str(exc), code="student_already_exists"
            ) from exc

    def update(self, instance: Student, validated_data: dict[str, Any]) -> Student:
        try:
            return update_student(
                student=instance,
                data=UpdateStudentData(
                    full_name=validated_data.get("full_name"),
                    gender=validated_data.get("gender"),
                    student_id=validated_data.get("student_id"),
                ),
            )
        except StudentAlreadyExistException as exc:
            raise serializers.ValidationError(
                str(exc), code="student_already_exists"
            ) from exc
