from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "tenant", "role", "is_staff")
    list_filter = ("tenant", "role", "is_staff")
    fieldsets = UserAdmin.fieldsets + (("Tenant", {"fields": ("tenant", "role")}),)
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2", "tenant", "role")}),)
    ordering = ("email",)
