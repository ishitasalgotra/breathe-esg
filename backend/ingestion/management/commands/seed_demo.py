from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tenants.models import Tenant
from emissions.models import NormalizationRule


class Command(BaseCommand):
    help = "Create a demo tenant, analyst user, and baseline normalization rules."

    def handle(self, *args, **options):
        tenant, _ = Tenant.objects.get_or_create(name="Breathe Demo Manufacturing")
        User = get_user_model()
        user, created = User.objects.get_or_create(email="analyst@example.com", defaults={"tenant": tenant, "role": "admin", "is_staff": True})
        if created:
            user.set_password("password123")
            user.save()
        auditor, created = User.objects.get_or_create(email="auditor@example.com", defaults={"tenant": tenant, "role": "auditor"})
        if created:
            auditor.set_password("password123")
            auditor.save()
        for source, target, factor in [("kWh", "MWh", "0.001"), ("MWh", "kWh", "1000"), ("liters", "gallons", "0.264172"), ("gallons", "liters", "3.78541"), ("miles", "km", "1.60934")]:
            NormalizationRule.objects.get_or_create(source_unit=source, target_unit=target, defaults={"conversion_factor": factor})
        self.stdout.write(self.style.SUCCESS("Demo tenant ready: analyst@example.com / password123 and auditor@example.com / password123"))
