from django.contrib import admin

from evaluation.models import (
    Assessment,
    AssessmentSubmission,
    AssessmentSubmissionQuestionAnswer,
    QuestionInfo,
)


class QuestionInfoInline(admin.TabularInline):
    model = QuestionInfo
    autocomplete_fields = ["question"]


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    autocomplete_fields = ["groups"]
    inlines = [
        QuestionInfoInline,
    ]


class AssessmentSubmissionQuestionAnswerInline(admin.StackedInline):
    model = AssessmentSubmissionQuestionAnswer


@admin.register(AssessmentSubmission)
class AssessmentSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "assessment",
        "author",
        "created_at",
        "updated_at",
    )

    inlines = [
        AssessmentSubmissionQuestionAnswerInline,
    ]
