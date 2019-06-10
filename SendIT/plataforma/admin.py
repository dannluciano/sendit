from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Question, Submission, CaseTest, Tags


class CaseTestInline(admin.TabularInline):
    model = CaseTest
    extra = 1

    fieldsets = (
        ("Teste", {"classes": ("collapse",), "fields": ("entrada", "saida")}),)


def esconder(modeladmin, request, queryset):
    queryset.update(exibir=False)


esconder.short_description = "Esconder Questões"


def exibir(modeladmin, request, queryset):
    queryset.update(exibir=True)


exibir.short_description = "Exibir Questões"


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("titulo", "enunciado", "xp", "tags", "exibir")}),
        (
            "Entrada e Saida (Exemplo)",
            {"classes": ("collapse",), "fields": ("entrada", "saida")},
        ),
    )

    inlines = [CaseTestInline]

    list_display = ("id", "titulo", "xp", "exibir")
    list_display_links = ("id", "titulo")
    search_fields = ["titulo"]

    actions = [esconder, exibir]

    save_as = True
    save_on_top = True

    list_editable = ("exibir",)

    class Media:
        js = ("js/ace.js", "js/admin.js")


class SubmissoesAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "autor",
                    "questao", "language", "timestamp")
    list_display_links = ("id", "status")
    list_filter = ("status", "language")
    search_fields = ["autor__username", "autor__email", "questao__titulo"]


class UserAdmin(BaseUserAdmin):
    list_display = ("username", "first_name", "is_staff", "is_superuser")

    # def get_xp(self, obj):
    #     return obj.perfil.xp
    # get_xp.short_description = 'XP'
    # get_xp.admin_order_field = 'perfil__xp'

    # def get_groups(self, obj):
    #     short_name = lambda n: str(n)
    #     groups = [short_name(group) for group in obj.groups.all()]
    #     return ', '.join(groups)
    # get_groups.short_description = 'Groups'


admin.site.register(Question, QuestionAdmin)
admin.site.register(Submission, SubmissoesAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Tags)
