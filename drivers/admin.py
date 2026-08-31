from django.contrib import admin

from .models import DriverProfile


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "license_type",
        "experience",
        "preferred_vehicle",
        "city",
        "state",
        "available",
        "is_verified",
        "is_profile_completed",
    )

    list_filter = (
        "license_type",
        "preferred_vehicle",
        "available",
        "is_verified",
        "is_profile_completed",
        "state",
    )

    search_fields = (
        "user__full_name",
        "user__email",
        "license_number",
        "city",
        "state",
    )

    ordering = ("-created_at",)