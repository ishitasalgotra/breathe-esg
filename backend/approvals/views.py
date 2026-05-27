from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from audit.services import write_audit
from emissions.models import ApprovalStatus, EmissionRecord
from users.permissions import IsAnalystOrAdmin
from .models import ApprovalWorkflow
from .serializers import ApprovalActionSerializer, ApprovalWorkflowSerializer


class ApprovalWorkflowViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ApprovalWorkflowSerializer
    permission_classes = [IsAnalystOrAdmin]

    def get_queryset(self):
        qs = ApprovalWorkflow.objects.select_related("record", "approved_by", "record__tenant")
        if self.request.user.is_superuser:
            return qs
        return qs.filter(record__tenant=self.request.user.tenant)

    @action(detail=False, methods=["get"])
    def queue(self, request):
        qs = EmissionRecord.objects.filter(approval_status=ApprovalStatus.PENDING).select_related("source")
        if not request.user.is_superuser:
            qs = qs.filter(tenant=request.user.tenant)
        from emissions.serializers import EmissionRecordSerializer
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(EmissionRecordSerializer(page, many=True).data)
        return Response(EmissionRecordSerializer(qs, many=True).data)

    @action(detail=False, methods=["post"], url_path="records/(?P<record_id>[^/.]+)/decision")
    @transaction.atomic
    def decision(self, request, record_id=None):
        serializer = ApprovalActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        record_qs = EmissionRecord.objects.select_for_update()
        if not request.user.is_superuser:
            record_qs = record_qs.filter(tenant=request.user.tenant)
        record = record_qs.get(id=record_id)
        before = {"approval_status": record.approval_status}
        record.approval_status = serializer.validated_data["status"]
        record.save(update_fields=["approval_status", "updated_at"])
        workflow = ApprovalWorkflow.objects.create(record=record, approved_by=request.user, status=record.approval_status, note=serializer.validated_data.get("note", ""))
        write_audit(tenant=record.tenant, entity_type="EmissionRecord", entity_id=record.id, action="approval_decision", before_value=before, after_value={"approval_status": record.approval_status, "workflow_id": workflow.id}, changed_by=request.user)
        return Response(ApprovalWorkflowSerializer(workflow).data, status=status.HTTP_201_CREATED)
