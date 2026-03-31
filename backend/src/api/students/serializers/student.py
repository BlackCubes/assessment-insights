from rest_framework import serializers

from apps.students.models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["uuid", "student_id", "full_name", "gender"]
