from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ("email", "tenant", "role", "is_staff")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Tenant Info", {"fields": ("tenant", "role")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "tenant", "role"),
        }),
    )

    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)