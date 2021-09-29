from django.contrib import admin

from .models import FileCode, Runner


class RunnerAdmin(admin.ModelAdmin):
    list_display = ("uuid", "status", "language", "timestamp")
    list_display_links = ("uuid", "status")
    list_filter = ("status", "language")


class FileCodeAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name", "owner", "language", "created_at", "updated_at")
    list_display_links = ("uuid", "name", )
    list_filter = ("language", )


admin.site.register(Runner, RunnerAdmin)
admin.site.register(FileCode, FileCodeAdmin)