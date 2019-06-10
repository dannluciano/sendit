from django.contrib import admin

from .models import LeaderboardView, StatisticsView


class LeaderboardViewAdmin(admin.ModelAdmin):
    list_display = ('position', 'username', 'xp')

    def has_add_permission(self, request):
        return False

    ordering = ('-xp', )


class StatisticsViewAdmin(admin.ModelAdmin):
    list_display = ('username', 'level', 'xp', 'number_of_submissions_ok', 'number_of_submission', 'conclusion_rate',
                    'sucess_rate', 'sintax_error_rate', 'runtime_error_rate', 'timeout_error_rate', 'diff_error_rate')

    def has_add_permission(self, request):
        return False


admin.site.register(LeaderboardView, LeaderboardViewAdmin)
admin.site.register(StatisticsView, StatisticsViewAdmin)
