from typing import Any

from rest_framework import serializers

from apps.academics.exceptions import PeriodAlreadyExistsException
from apps.academics.models import Period
from apps.academics.services import (
    CreatePeriodData,
    UpdatePeriodData,
    create_period,
    update_period,
)


class PeriodSerializer(serializers.ModelSerializer[Period]):
    name = serializers.CharField(max_length=20)
    period_number = serializers.IntegerField(min_value=1)

    class Meta:
        model = Period
        fields = ["uuid", "name", "period_number", "created_at", "updated_at"]
        read_only_fields = ["uuid", "created_at", "updated_at"]

    def create(self, validated_data: dict[str, Any]) -> Period:
        try:
            return create_period(
                data=CreatePeriodData(
                    name=validated_data["name"],
                    period_number=validated_data["period_number"],
                )
            )
        except PeriodAlreadyExistsException as exc:
            raise serializers.ValidationError(
                str(exc), code="period_already_exists"
            ) from exc

    def update(self, instance: Period, validated_data: dict[str, Any]) -> Period:
        try:
            return update_period(
                period=instance,
                data=UpdatePeriodData(
                    name=validated_data.get("name"),
                    period_number=validated_data.get("period_number"),
                ),
            )
        except PeriodAlreadyExistsException as exc:
            raise serializers.ValidationError(
                str(exc), code="period_already_exists"
            ) from exc
