from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("emissions", "0001_initial"), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name="ApprovalWorkflow", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("approved_at", models.DateTimeField(auto_now_add=True)), ("status", models.CharField(choices=[("approved", "Approved"), ("rejected", "Rejected")], max_length=20)), ("note", models.TextField(blank=True)), ("approved_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="approval_events", to=settings.AUTH_USER_MODEL)), ("record", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="approval_events", to="emissions.emissionrecord"))], options={"ordering": ["-approved_at"]})]
