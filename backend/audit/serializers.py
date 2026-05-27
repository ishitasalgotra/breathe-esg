from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    changed_by_email = serializers.EmailField(source="changed_by.email", read_only=True)

    class Meta:
        model = AuditLog
        fields = ["id", "tenant", "entity_type", "entity_id", "action", "before_value", "after_value", "changed_by", "changed_by_email", "timestamp"]
        read_only_fields = fields
