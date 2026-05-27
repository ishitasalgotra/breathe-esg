from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("admin", "Admin"),
                    ("analyst", "Analyst"),
                    ("auditor", "Auditor"),
                    ("viewer", "Viewer"),
                ],
                default="analyst",
                max_length=20,
            ),
        ),
    ]
