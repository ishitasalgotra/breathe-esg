from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()

        if not User.objects.filter(email="admin@example.com").exists():
            User.objects.create_superuser(
                email="admin@example.com",
                password="Admin@12345"
            )

        if not User.objects.filter(email="analyst@example.com").exists():
            User.objects.create_user(
                email="analyst@example.com",
                password="Password@12345"
            )