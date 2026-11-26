from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.core.mail import send_mail
from django.contrib import messages

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
    def save_model(self, request, obj, form, change):
        was_approved = False

        if change:
            old_user = User.objects.get(pk=obj.pk)
            was_approved = old_user.is_approved

        if obj.is_approved:
            obj.is_active = True

        super().save_model(request, obj, form, change)

        if obj.is_approved and not was_approved:
            try:
                send_mail(
                    subject="Your SnapShare Account is Approved!",
                    message=(
                        f"Hello {obj.first_name},\n\n"
                        "Your SnapShare account has been approved. "
                        "You can now log in using your registered email "
                        "and password.\n\n"
                        "Welcome to SnapShare!"
                    ),
                    from_email=None,
                    recipient_list=[obj.email],
                    fail_silently=False,
                )

                self.message_user(
                    request,
                    f"Approval email sent to {obj.email}."
                )

            except Exception:
                self.message_user(
                    request,
                    "Account approved, but the email could not be sent.",
                    level=messages.WARNING,
                )