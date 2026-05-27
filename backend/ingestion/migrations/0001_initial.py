from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("tenants", "0001_initial")]
    operations = [
        migrations.CreateModel(name="DataSource", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("source_type", models.CharField(choices=[("sap", "SAP procurement/fuel"), ("utility", "Utility electricity"), ("travel", "Corporate travel")], max_length=30)), ("uploaded_at", models.DateTimeField(auto_now_add=True)), ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="data_sources", to="tenants.tenant")), ("uploaded_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="data_sources", to=settings.AUTH_USER_MODEL))], options={"ordering": ["-uploaded_at"]}),
        migrations.CreateModel(name="RawUpload", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("original_filename", models.CharField(max_length=255)), ("source_type", models.CharField(choices=[("sap", "SAP procurement/fuel"), ("utility", "Utility electricity"), ("travel", "Corporate travel")], max_length=30)), ("upload_status", models.CharField(choices=[("received", "Received"), ("processing", "Processing"), ("completed", "Completed"), ("completed_with_warnings", "Completed with warnings"), ("failed", "Failed")], default="received", max_length=40)), ("raw_file_path", models.FileField(upload_to="uploads/%Y/%m/%d/")), ("row_count", models.PositiveIntegerField(default=0)), ("error_count", models.PositiveIntegerField(default=0)), ("summary", models.JSONField(blank=True, default=dict)), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)), ("data_source", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="raw_upload", to="ingestion.datasource")), ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="raw_uploads", to="tenants.tenant"))], options={"ordering": ["-created_at"]}),
        migrations.AddIndex(model_name="datasource", index=models.Index(fields=["tenant", "source_type"], name="ingestion_d_tenant__d9aeda_idx")),
        migrations.AddIndex(model_name="rawupload", index=models.Index(fields=["tenant", "source_type", "upload_status"], name="ingestion_r_tenant__ff3cab_idx")),
    ]
