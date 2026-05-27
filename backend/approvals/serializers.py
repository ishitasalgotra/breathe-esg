from rest_framework import serializers
from .models import ApprovalWorkflow


class ApprovalWorkflowSerializer(serializers.ModelSerializer):
    approved_by_email = serializers.EmailField(source="approved_by.email", read_only=True)

    class Meta:
        model = ApprovalWorkflow
        fields = ["id", "record", "approved_by", "approved_by_email", "approved_at", "status", "note"]
        read_only_fields = ["id", "approved_by", "approved_by_email", "approved_at"]


class ApprovalActionSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[("approved", "Approved"), ("rejected", "Rejected")])
    note = serializers.CharField(required=False, allow_blank=True)
