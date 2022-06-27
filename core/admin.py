from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.safestring import mark_safe

from core.domain import get_user_profile
from core.models import CaseTest, Question, Submission, Tags


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


def compare_submissions(modeladmin, request, queryset):
    queryset = queryset.order_by('timestamp')
    
    context = dict(
        modeladmin.admin_site.each_context(request),
        submissions=queryset,
        submissions_size=len(queryset),
    )

    return render(
        request,
        "admin/diff.html",
        context,
    )


compare_submissions.short_description = "Comparar Submissões"


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

    list_filter = (
        "status",
        "language",
        "timestamp",
        "question__tags",
        "author__groups",
    )

    search_fields = (
        "author__username",
        "author__email",
        "question__title",
    )

    actions = (
        compare_submissions,
    )


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
        return mark_safe(
            "<a class='button' href='/admin/auth/user/profile/%s/'>Perfil</a>" % obj.id
        )

    profile_link.short_description = "Perfil"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("profile/<int:user_id>/", self.profile_view, name="profile_view"),
        ]
        return my_urls + urls

    def profile_view(self, request, user_id):
        if request.user.is_staff:
            profile = get_user_profile(user_id)
            context = dict(
                self.admin_site.each_context(request),
                profile=profile,
            )

            return render(request, "admin/profile.html", context)
        return redirect(settings.LOGIN_URL)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Submission, SubmissionsAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Tags)
