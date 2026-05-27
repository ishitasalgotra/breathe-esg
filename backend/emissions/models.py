from django.db import models


class ApprovalStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class NormalizationRule(models.Model):
    source_unit = models.CharField(max_length=40)
    target_unit = models.CharField(max_length=40)
    conversion_factor = models.DecimalField(max_digits=18, decimal_places=8)

    class Meta:
        unique_together = ("source_unit", "target_unit")

    def __str__(self):
        return f"{self.source_unit} -> {self.target_unit}"


class EmissionRecord(models.Model):
    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="emission_records")
    source = models.ForeignKey("ingestion.DataSource", on_delete=models.CASCADE, related_name="emission_records")
    scope_category = models.CharField(max_length=80)
    emission_category = models.CharField(max_length=120)
    raw_value = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    raw_unit = models.CharField(max_length=40, blank=True)
    normalized_value = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    normalized_unit = models.CharField(max_length=40, blank=True)
    source_row_reference = models.CharField(max_length=120)
    suspicious_flag = models.BooleanField(default=False)
    suspicious_reasons = models.JSONField(default=list, blank=True)
    approval_status = models.CharField(max_length=20, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["tenant", "approval_status"]), models.Index(fields=["tenant", "suspicious_flag"]), models.Index(fields=["source", "source_row_reference"])]
        ordering = ["-created_at"]
