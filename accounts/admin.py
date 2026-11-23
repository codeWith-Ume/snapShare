from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):

    ordering = ("email",)

    list_display = (
        "email",
        "first_name",
        "is_approved",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "is_approved",
        "is_active",
        "is_staff",
    )

    search_fields = ("email", "first_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name",)}),
        ("Approval", {"fields": ("is_approved", "is_active", "is_email_verified")}),
        ("Permissions", {
            "fields": (
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "password1", "password2"),
        }),
    )