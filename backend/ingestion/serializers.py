from rest_framework import serializers
from .models import DataSource, RawUpload, SourceType


class DataSourceSerializer(serializers.ModelSerializer):
    uploaded_by_email = serializers.EmailField(source="uploaded_by.email", read_only=True)

    class Meta:
        model = DataSource
        fields = ["id", "tenant", "source_type", "uploaded_by", "uploaded_by_email", "uploaded_at"]
        read_only_fields = ["id", "tenant", "uploaded_by", "uploaded_at"]


class RawUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawUpload
        fields = ["id", "tenant", "data_source", "original_filename", "source_type", "upload_status", "raw_file_path", "row_count", "error_count", "summary", "created_at", "updated_at"]
        read_only_fields = ["id", "tenant", "data_source", "upload_status", "row_count", "error_count", "summary", "created_at", "updated_at"]


class UploadCreateSerializer(serializers.Serializer):
    source_type = serializers.ChoiceField(choices=SourceType.choices)
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.lower().endswith(".csv"):
            raise serializers.ValidationError("Only CSV files are supported for this MVP ingestion pipeline.")
        return value
