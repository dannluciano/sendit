from django.contrib import admin

from .models import LeaderboardView, StatisticsView, SubmissionSummaryView


class ViewAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        return None

    def has_add_permission(self, request):
        return False

    def has_change_permission(request, obj=None):
        return False


class LeaderboardViewAdmin(ViewAdmin):
    list_display = ('position', 'username', 'xp', 'level')

    ordering = ('-xp', )


class StatisticsViewAdmin(ViewAdmin):
    list_display = ('username', 'level', 'xp', 'number_of_submissions_ok', 'number_of_submission', 'conclusion_rate',
                    'sucess_rate', 'sintax_error_rate', 'runtime_error_rate', 'timeout_error_rate', 'diff_error_rate')


class SubmissionSummaryViewAdmin(ViewAdmin):
    list_display = ('status', 'sum')


admin.site.register(LeaderboardView, LeaderboardViewAdmin)
admin.site.register(StatisticsView, StatisticsViewAdmin)
admin.site.register(SubmissionSummaryView, SubmissionSummaryViewAdmin)
