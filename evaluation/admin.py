from django.contrib import admin
from django.utils import timezone

from evaluation.models import (
    Assessment,
    AssessmentSubmission,
    QuestionInfo,
)


class QuestionInfoInline(admin.StackedInline):
    model = QuestionInfo
    extra = 1
    autocomplete_fields = ["question"]


class IsAvaliableListFilter(admin.SimpleListFilter):
    title = "Filtro de Disponibilidade"

    parameter_name = "is_available"

    def lookups(self, request, model_admin):
        return [
            ("1", "Dispoível"),
            ("0", "Não Dispoível"),
        ]

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == "0":
            return queryset.exclude(date_start__lt=now, date_end__gt=now)
        if self.value() == "1":
            return queryset.filter(date_start__lt=now, date_end__gt=now)


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_available",
        "total_of_points",
        "date_start",
        "date_end",
    )

    list_filter = (
        "date_start",
        IsAvaliableListFilter,
    )

    autocomplete_fields = ["groups"]
    inlines = [
        QuestionInfoInline,
    ]


class ScoreListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = "Filtro de Notas"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "score"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
            ("4", "0,0 ~ 4,0"),
            ("7", "4,0 ~ 7,0"),
            ("10", "7,0 ~ 10,0"),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        print(self.value())
        if self.value() == "4":
            return queryset.filter(
                score__gte=0,
                score__lt=4,
            )
        if self.value() == "7":
            return queryset.filter(
                score__gte=4,
                score__lt=7,
            )
        if self.value() == "10":
            return queryset.filter(
                score__gte=7,
                score__lt=10,
            )


def compute_score(modeladmin, request, queryset):
    objs = queryset.all()
    for obj in objs:
        obj.compute_score()


compute_score.short_description = "Calcular Nota"


@admin.register(AssessmentSubmission)
class AssessmentSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "assessment",
        "full_name",
        "score",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "assessment",
        "author",
        "score",
    )

    list_filter = [
        "assessment",
        ScoreListFilter,
    ]

    actions = [
        compute_score,
    ]

    @admin.display(description="Nome Completo")
    def full_name(self, obj):
        name = f"{obj.author.first_name} {obj.author.last_name}".upper()
        username = obj.author.username
        return f"{name} - @{username}"
