from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Question, Submission, CaseTest, Perfil
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
    search_fields = ['autor__username', 'autor__email', 'questao__titulo']


class SubmissionSummaryAdmin(admin.ModelAdmin):
    list_display = ('status', 'sum')
    list_display_links = None
    actions = None

    def has_add_permission(self, request):
        return False


class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'perfil'


class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline, )


class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'xp',
                    'taxa_de_conclusao', 'taxa_de_sucesso',
                    'submissoes', 'acertos',
                    'erros_de_sintax', 'erros_de_execucao',
                    'erros_de_tempo', 'erros_de_saida')
    list_display_links = None
    list_filter = ('user__groups',)
    search_fields = ['user__username', 'user__email']

    def has_add_permission(self, request):
        return False


admin.site.register(Question, QuestionAdmin)
admin.site.register(Submission, SubmissoesAdmin)
admin.site.register(SubmissionSummary, SubmissionSummaryAdmin)
admin.site.register(Perfil, PerfilAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
