from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("ingestion", "0001_initial"), ("tenants", "0001_initial")]
    operations = [
        migrations.CreateModel(name="NormalizationRule", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("source_unit", models.CharField(max_length=40)), ("target_unit", models.CharField(max_length=40)), ("conversion_factor", models.DecimalField(decimal_places=8, max_digits=18))], options={"unique_together": {("source_unit", "target_unit")}}),
        migrations.CreateModel(name="EmissionRecord", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("scope_category", models.CharField(max_length=80)), ("emission_category", models.CharField(max_length=120)), ("raw_value", models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)), ("raw_unit", models.CharField(blank=True, max_length=40)), ("normalized_value", models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)), ("normalized_unit", models.CharField(blank=True, max_length=40)), ("source_row_reference", models.CharField(max_length=120)), ("suspicious_flag", models.BooleanField(default=False)), ("suspicious_reasons", models.JSONField(blank=True, default=list)), ("approval_status", models.CharField(choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending", max_length=20)), ("metadata", models.JSONField(blank=True, default=dict)), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)), ("source", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="emission_records", to="ingestion.datasource")), ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="emission_records", to="tenants.tenant"))], options={"ordering": ["-created_at"]}),
        migrations.AddIndex(model_name="emissionrecord", index=models.Index(fields=["tenant", "approval_status"], name="emissions_e_tenant__cd4dc0_idx")),
        migrations.AddIndex(model_name="emissionrecord", index=models.Index(fields=["tenant", "suspicious_flag"], name="emissions_e_tenant__713624_idx")),
        migrations.AddIndex(model_name="emissionrecord", index=models.Index(fields=["source", "source_row_reference"], name="emissions_e_source__d72f86_idx")),
    ]
