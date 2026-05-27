from django.conf import settings
from django.db import models


class WorkflowStatus(models.TextChoices):
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class ApprovalWorkflow(models.Model):
    record = models.ForeignKey("emissions.EmissionRecord", on_delete=models.CASCADE, related_name="approval_events")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="approval_events")
    approved_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=WorkflowStatus.choices)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["-approved_at"]
