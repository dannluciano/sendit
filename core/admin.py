from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import render

from core.domain import get_user_profile
from .models import Question, Submission, CaseTest, Tags
from django.utils.safestring import mark_safe
from django.urls import path


class CaseTestInline(admin.TabularInline):
    model = CaseTest
    extra = 1

    fieldsets = (
        (
            "Teste",
            {"classes": ("collapse",), "fields": ("sample_input", "sample_output")},
        ),
    )


def hide(modeladmin, request, queryset):
    queryset.update(visible=False)


hide.short_description = "Esconder Questões"


def show(modeladmin, request, queryset):
    queryset.update(visible=True)


show.short_description = "Exibir Questões"


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("title", "statement", "xp", "tags", "visible")}),
        (
            "Entrada e Saida (Exemplo)",
            {"classes": ("collapse",), "fields": ("sample_input", "sample_output")},
        ),
    )

    inlines = [CaseTestInline]

    list_display = ("id", "title", "xp", "visible")
    list_display_links = ("id", "title")
    list_filter = ("tags",)
    search_fields = ["title"]

    actions = [hide, show]

    save_as = True
    save_on_top = True


class SubmissionsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "uuid",
        "status",
        "author",
        "question",
        "language",
        "timestamp",
    )
    list_display_links = ("id", "status")
    list_filter = ("status", "language")
    search_fields = ["author__username", "author__email", "question__title"]


class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "profile_link",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_superuser",
        "last_login",
    )
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )
    list_filter = BaseUserAdmin.list_filter + ("last_login",)

    def profile_link(self, obj):
        return mark_safe("<a href='/admin/auth/user/profile/%s/'>Profile</a>" % obj.id)

    profile_link.short_description = "Profile"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("profile/<int:user_id>/", self.profile_view, name="profile_view"),
        ]
        return my_urls + urls

    def profile_view(self, request, user_id):
        profile = get_user_profile(user_id)

        return render(request, "admin/profile.html", {"profile": profile})

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
admin.site.register(Submission, SubmissionsAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Tags)
