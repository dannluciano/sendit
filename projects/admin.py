from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "created_at",
        "updated_at",
    )

    fields = (
        "name",
        "owner",
        "container_id",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "container_id",
        "created_at",
        "updated_at",
    )
