from rest_framework import viewsets
from users.permissions import IsTenantMember
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [IsTenantMember]
    filterset_fields = ["entity_type", "entity_id", "action"]
    search_fields = ["entity_type", "entity_id", "action", "changed_by__email"]
    ordering_fields = ["timestamp"]

    def get_queryset(self):
        qs = AuditLog.objects.select_related("tenant", "changed_by")
        if self.request.user.is_superuser:
            return qs
        return qs.filter(tenant=self.request.user.tenant)
