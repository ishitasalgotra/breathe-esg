from rest_framework import viewsets
from users.permissions import IsTenantAdmin
from .models import Tenant
from .serializers import TenantSerializer


class TenantViewSet(viewsets.ModelViewSet):
    serializer_class = TenantSerializer
    permission_classes = [IsTenantAdmin]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Tenant.objects.all()
        return Tenant.objects.filter(id=self.request.user.tenant_id)
