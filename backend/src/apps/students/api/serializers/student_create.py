from rest_framework import serializers

from apps.students.models import Student
from apps.students.services import CreateStudentData, create_student


class StudentCreateSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=Student.full_name.max_length)
    gender = serializers.CharField(
        max_length=Student.gender.max_length, choices=Student.GenderTypes.choices
    )
    student_id = serializers.CharField(max_length=Student.student_id.max_length)

    def create(self, validated_data: dict[str, str]) -> Student:
        return create_student(
            data=CreateStudentData(
                full_name=validated_data["full_name"],
                gender=validated_data["gender"],
                student_id=validated_data["student_id"],
            )
        )
