from typing import Any

from rest_framework import serializers

from apps.academics.exceptions import TermAlreadyExistsException
from apps.academics.models import Term
from apps.academics.services import (
    CreateTermData,
    UpdateTermData,
    create_term,
    update_term,
)


class TermSerializer(serializers.ModelSerializer[Term]):
    name = serializers.CharField(max_length=20)
    school_year = serializers.CharField(max_length=20)
    semester = serializers.IntegerField(min_value=1, max_value=2)

    class Meta:
        model = Term
        fields = ["uuid", "name", "school_year", "semester", "created_at", "updated_at"]
        read_only_fields = ["uuid", "created_at", "updated_at"]

    def create(self, validated_data: dict[str, Any]) -> Term:
        try:
            return create_term(
                data=CreateTermData(
                    name=validated_data["name"],
                    school_year=validated_data["school_year"],
                    semester=validated_data["semester"],
                )
            )
        except TermAlreadyExistsException as exc:
            raise serializers.ValidationError(
                str(exc), code="term_already_exists"
            ) from exc

    def update(self, instance: Term, validated_data: dict[str, Any]) -> Term:
        try:
            return update_term(
                term=instance,
                data=UpdateTermData(
                    name=validated_data.get("name"),
                    school_year=validated_data["school_year"],
                    semester=validated_data["semester"],
                ),
            )
        except TermAlreadyExistsException as exc:
            raise serializers.ValidationError(str(exc), code="term") from exc
