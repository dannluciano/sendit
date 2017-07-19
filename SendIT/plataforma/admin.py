from django.contrib import admin
from .models import Question, Submission, CaseTest
from .models import SubmissionSummary


class CaseTestInline(admin.TabularInline):
    model = CaseTest
    extra = 1

    fieldsets = (
        ('Teste', {
            'classes': ('collapse',),
            'fields': ('entrada', 'saida')
        }),
    )


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('titulo', 'enunciado', 'xp', 'tags')
        }),
        ('Entrada e Saida (Exemplo)', {
            'classes': ('collapse',),
            'fields': ('entrada', 'saida'),
        }),
        ('Pré Codigo', {
            'classes': ('collapse',),
            'fields': ('pre_codigo',),
        }),
        ('Pos Codigo', {
            'classes': ('collapse',),
            'fields': ('pos_codigo',),
        }),
    )

    inlines = [
        CaseTestInline,
    ]

    class Media:
        js = ('js/ace.js', 'js/admin.js',)


class SubmissoesAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'autor', 'questao')
    list_display_links = ('id', 'status')
    list_filter = ('status',)
    search_fields = ['autor__email', 'status']


class SubmissionSummaryAdmin(admin.ModelAdmin):
    list_display = ('status', 'sum')
    list_display_links = None
    actions = None

    def has_add_permission(self, request):
        return False


admin.site.register(Question, QuestionAdmin)
admin.site.register(Submission, SubmissoesAdmin)
admin.site.register(SubmissionSummary, SubmissionSummaryAdmin)
