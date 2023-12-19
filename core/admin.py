import tarfile
from datetime import datetime
from tempfile import mkdtemp

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.safestring import mark_safe

from core.domain import get_user_profile
from core.models import Achievement, CaseTest, Question, Submission, Tags


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

    class Media:
        css = {"all": ("css/admin.css",)}


def compare_submissions(modeladmin, request, queryset):
    queryset = queryset.order_by("timestamp")

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


def download_submissions(modeladmin, request, queryset):
    unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()

    extension_dict = {
        "c": "c",
        "cplusplus": "cpp",
        "javascript": "js",
        "java": "java",
        "python": "py",
    }

    temp_dir_path = mkdtemp()

    print(temp_dir_path)

    for submission in queryset:
        author = submission.author
        question = submission.question
        submission_id = submission.uuid
        extension = extension_dict[submission.language]
        file_name = f"{author}-{question}-{submission_id}.{extension}"
        file_path = f"{temp_dir_path}/{file_name}"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(submission.code)

    tarfile_name = f"{temp_dir_path}/{unix_timestamp}.tar"

    with tarfile.open(tarfile_name, "a:") as tar:
        tar.add(temp_dir_path, arcname="submissões")

    response = FileResponse(open(tarfile_name, "rb"), filename=f"{unix_timestamp}.tar")
    return response


download_submissions.short_description = "Baixar Submissões"


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

    actions = (compare_submissions, download_submissions)


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


class AchievementAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "badge_tag",
        "xp",
    )

    readonly_fields = ("badge_tag",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "badge",
                    "badge_tag",
                    "xp",
                    "users",
                )
            },
        ),
    )

    filter_horizontal = ("users",)

    list_filter = ("hidden",)

    ordering = ("hidden",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if "hidden__exact=1" in request.META["QUERY_STRING"]:
            return qs
        return qs.filter(hidden=False)

    def badge_tag(self, obj):
        return mark_safe(
            "<img class='image' src='%s' width='32px' height='32px'/>" % obj.badge.url
        )

    badge_tag.short_description = "Badge Image"


admin.site.register(Question, QuestionAdmin)
admin.site.register(Submission, SubmissionsAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Tags)
admin.site.register(Achievement, AchievementAdmin)
