from django.conf import settings
from django.db import models


class SourceType(models.TextChoices):
    SAP = "sap", "SAP procurement/fuel"
    UTILITY = "utility", "Utility electricity"
    TRAVEL = "travel", "Corporate travel"


class UploadStatus(models.TextChoices):
    RECEIVED = "received", "Received"
    PROCESSING = "processing", "Processing"
    COMPLETED = "completed", "Completed"
    COMPLETED_WITH_WARNINGS = "completed_with_warnings", "Completed with warnings"
    FAILED = "failed", "Failed"


class DataSource(models.Model):
    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="data_sources")
    source_type = models.CharField(max_length=30, choices=SourceType.choices)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="data_sources")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["tenant", "source_type"])]
        ordering = ["-uploaded_at"]


class RawUpload(models.Model):
    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="raw_uploads")
    data_source = models.OneToOneField(DataSource, on_delete=models.CASCADE, related_name="raw_upload")
    original_filename = models.CharField(max_length=255)
    source_type = models.CharField(max_length=30, choices=SourceType.choices)
    upload_status = models.CharField(max_length=40, choices=UploadStatus.choices, default=UploadStatus.RECEIVED)
    raw_file_path = models.FileField(upload_to="uploads/%Y/%m/%d/")
    row_count = models.PositiveIntegerField(default=0)
    error_count = models.PositiveIntegerField(default=0)
    summary = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["tenant", "source_type", "upload_status"])]
        ordering = ["-created_at"]
