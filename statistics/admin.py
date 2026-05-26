from django.contrib import admin

from .models import LogRecord


class ViewAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        return None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class LogRecordAdmin(ViewAdmin):
    date_hierarchy = "check_in"
    list_display = (
        "user",
        "ip",
        "check_in",
        "check_out",
        "duration",
    )
    list_filter = (
        "check_in",
        "check_out",
    )
    ordering = ["-check_in"]
    search_fields = (
        "user",
        "ip",
    )


admin.site.register(LogRecord, LogRecordAdmin)
