from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Question, Submission, CaseTest, Perfil, Tags, SubmissionSummary


class CaseTestInline(admin.TabularInline):
    model = CaseTest
    extra = 1

    fieldsets = (
        ('Teste', {
            'classes': ('collapse',),
            'fields': ('entrada', 'saida')
        }),
    )


def esconder(modeladmin, request, queryset):
    queryset.update(exibir=False)
esconder.short_description = "Esconder Questões"


def exibir(modeladmin, request, queryset):
    queryset.update(exibir=True)
exibir.short_description = "Exibir Questões"


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('titulo', 'enunciado', 'xp', 'tags', 'exibir')
        }),
        ('Entrada e Saida (Exemplo)', {
            'classes': ('collapse',),
            'fields': ('entrada', 'saida'),
        }),
    )

    inlines = [
        CaseTestInline,
    ]

    list_display = ('id', 'titulo', 'xp', 'exibir')
    list_display_links = ('id', 'titulo')
    search_fields = ['titulo',] 

    actions = [esconder, exibir]

    save_as = True
    save_on_top = True

    class Media:
        js = ('js/ace.js', 'js/admin.js',)


class SubmissoesAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'autor', 'questao', 'timestamp')
    list_display_links = ('id', 'status')
    list_filter = ('status',)
    search_fields = ['autor__username', 'autor__email', 'questao__titulo']


class SubmissionSummaryAdmin(admin.ModelAdmin):
    list_display = ('status', 'sum')
    list_display_links = None
    actions = None

    def has_add_permission(self, request):
        return False


class SubmissionInline(admin.StackedInline):
    model = Submission
    extra = 0
    verbose_name_plural = 'Submissões'


class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'perfil'


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'is_staff', 'is_superuser')
    inlines = (PerfilInline, )

    # def get_xp(self, obj):
    #     return obj.perfil.xp
    # get_xp.short_description = 'XP'
    # get_xp.admin_order_field = 'perfil__xp'

    # def get_groups(self, obj):
    #     short_name = lambda n: str(n)
    #     groups = [short_name(group) for group in obj.groups.all()]
    #     return ', '.join(groups)
    # get_groups.short_description = 'Groups'



class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'xp',
                    'tx_conclusao', 'tx_sucesso',
                    'submissoes', 'acertos',
                    'erros_de_sintax', 'erros_de_execucao',
                    'erros_de_tempo', 'erros_de_saida')
    list_display_links = ('user',)
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
admin.site.register(Tags)
