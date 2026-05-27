from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("tenants", "0001_initial")]
    operations = [
        migrations.CreateModel(name="AuditLog", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("entity_type", models.CharField(max_length=80)), ("entity_id", models.CharField(max_length=80)), ("action", models.CharField(max_length=80)), ("before_value", models.JSONField(blank=True, null=True)), ("after_value", models.JSONField(blank=True, null=True)), ("timestamp", models.DateTimeField(auto_now_add=True)), ("changed_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="audit_logs", to=settings.AUTH_USER_MODEL)), ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="audit_logs", to="tenants.tenant"))], options={"ordering": ["-timestamp"]}),
        migrations.AddIndex(model_name="auditlog", index=models.Index(fields=["tenant", "entity_type", "entity_id"], name="audit_audit_tenant__38d477_idx")),
        migrations.AddIndex(model_name="auditlog", index=models.Index(fields=["timestamp"], name="audit_audit_timesta_023417_idx")),
    ]
