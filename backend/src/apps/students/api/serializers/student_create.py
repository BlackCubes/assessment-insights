from rest_framework import serializers

from apps.students.models import Student
from apps.students.services import CreateStudentData, create_student


class StudentCreateSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    gender = serializers.ChoiceField(choices=["M", "F", "O"])
    student_id = serializers.CharField(max_length=10)

    def create(self, validated_data: dict[str, str]) -> Student:
        return create_student(
            data=CreateStudentData(
                full_name=validated_data["full_name"],
                gender=validated_data["gender"],
                student_id=validated_data["student_id"],
            )
        )
