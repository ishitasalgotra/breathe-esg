from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.permissions import IsAnalystOrAdmin, IsTenantMember
from .models import DataSource, RawUpload
from .serializers import RawUploadSerializer, UploadCreateSerializer
from .services.pipeline import process_upload


class RawUploadViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = RawUploadSerializer
    permission_classes = [IsTenantMember]

    filterset_fields = ["source_type", "upload_status"]
    search_fields = ["original_filename"]

    def get_queryset(self):
        qs = RawUpload.objects.select_related(
            "tenant",
            "data_source",
            "data_source__uploaded_by"
        )

        if self.request.user.is_superuser:
            return qs

        return qs.filter(tenant=self.request.user.tenant)

    def get_serializer_class(self):
        return (
            UploadCreateSerializer
            if self.action == "create"
            else RawUploadSerializer
        )

    def get_permissions(self):
        if self.action == "create":
            return [IsAnalystOrAdmin()]

        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            data_source = DataSource.objects.create(
                tenant=request.user.tenant,
                source_type=serializer.validated_data["source_type"],
                uploaded_by=request.user,
            )

            upload = RawUpload.objects.create(
                tenant=request.user.tenant,
                data_source=data_source,
                source_type=data_source.source_type,
                original_filename=serializer.validated_data["file"].name,
                raw_file_path=serializer.validated_data["file"],
            )

            process_upload(upload, request.user)

            return Response(
                RawUploadSerializer(
                    upload,
                    context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            import traceback

            print(traceback.format_exc())

            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def status(self, request):
        qs = self.get_queryset()

        return Response(
            {
                "total_uploads": qs.count(),
                "by_status": {
                    s: qs.filter(upload_status=s).count()
                    for s in qs.values_list(
                        "upload_status",
                        flat=True
                    ).distinct()
                },
            }
        )