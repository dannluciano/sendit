from django.contrib import admin

from .models import Runner


class RunnerAdmin(admin.ModelAdmin):
    list_display = ("uuid", "status", "language", "timestamp")
    list_display_links = ("uuid", "status")
    list_filter = ("status", "language")


admin.site.register(Runner, RunnerAdmin)