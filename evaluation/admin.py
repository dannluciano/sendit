from django.contrib import admin

from evaluation.models import (
    Assessment,
    AssessmentSubmission,
    QuestionInfo,
)


class QuestionInfoInline(admin.TabularInline):
    model = QuestionInfo
    autocomplete_fields = ["question"]


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("name", "total_of_points", "date_start", "date_end")

    autocomplete_fields = ["groups"]
    inlines = [
        QuestionInfoInline,
    ]


def compute_score(modeladmin, request, queryset):
    objs = queryset.all()
    for obj in objs:
        obj.compute_score()


compute_score.short_description = "Calcular Nota"


@admin.register(AssessmentSubmission)
class AssessmentSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "assessment",
        "author",
        "score",
        "created_at",
        "updated_at",
    )

    list_filter = ("assessment",)

    actions = [
        compute_score,
    ]
