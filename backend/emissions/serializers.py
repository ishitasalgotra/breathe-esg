from rest_framework import serializers
from .models import EmissionRecord, NormalizationRule


class EmissionRecordSerializer(serializers.ModelSerializer):
    source_type = serializers.CharField(source="source.source_type", read_only=True)

    class Meta:
        model = EmissionRecord
        fields = ["id", "tenant", "source", "source_type", "scope_category", "emission_category", "raw_value", "raw_unit", "normalized_value", "normalized_unit", "source_row_reference", "suspicious_flag", "suspicious_reasons", "approval_status", "metadata", "created_at", "updated_at"]
        read_only_fields = fields


class NormalizationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalizationRule
        fields = ["id", "source_unit", "target_unit", "conversion_factor"]
