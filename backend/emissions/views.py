from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.permissions import IsAnalystOrAdmin, IsTenantMember
from .models import ApprovalStatus, EmissionRecord, NormalizationRule
from .serializers import EmissionRecordSerializer, NormalizationRuleSerializer


class EmissionRecordViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EmissionRecordSerializer
    permission_classes = [IsTenantMember]
    filterset_fields = ["approval_status", "suspicious_flag", "scope_category", "emission_category", "source__source_type"]
    search_fields = ["source_row_reference", "emission_category", "metadata"]
    ordering_fields = ["created_at", "updated_at", "normalized_value"]

    def get_queryset(self):
        qs = EmissionRecord.objects.select_related("tenant", "source")
        if not self.request.user.is_superuser:
            qs = qs.filter(tenant=self.request.user.tenant)
        return qs

    @action(detail=False, methods=["get"])
    def suspicious(self, request):
        page = self.paginate_queryset(self.get_queryset().filter(suspicious_flag=True))
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(self.get_queryset().filter(suspicious_flag=True), many=True).data)

    @action(detail=False, methods=["get"])
    def dashboard(self, request):
        qs = self.get_queryset()
        return Response({"total_records": qs.count(), "suspicious_records": qs.filter(suspicious_flag=True).count(), "approved_records": qs.filter(approval_status=ApprovalStatus.APPROVED).count(), "pending_approvals": qs.filter(approval_status=ApprovalStatus.PENDING).count(), "ingestion_statistics": list(qs.values("source__source_type").annotate(count=Count("id")).order_by("source__source_type"))})


class NormalizationRuleViewSet(viewsets.ModelViewSet):
    serializer_class = NormalizationRuleSerializer
    permission_classes = [IsTenantMember]
    queryset = NormalizationRule.objects.all().order_by("source_unit")

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [IsAnalystOrAdmin()]
        return super().get_permissions()
