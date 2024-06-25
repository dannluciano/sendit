import uuid

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from core.models import Question, Submission


class Assessment(models.Model):
    uuid = models.UUIDField(
        "uuid",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    name = models.CharField("Nome", max_length=255)

    groups = models.ManyToManyField("auth.Group", verbose_name="Turmas")

    date_start = models.DateTimeField(
        "Data de Início", auto_now=False, auto_now_add=False
    )

    date_end = models.DateTimeField(
        "Data de Fim", auto_now=False, auto_now_add=False
    )

    description = RichTextField("Descrição")

    questions = models.ManyToManyField(
        Question, verbose_name="Questões", through="QuestionInfo"
    )

    def is_available(self):
        now = timezone.now()
        return self.date_start < now and now < self.date_end

    is_available.boolean = True
    is_available.short_description = "Disponível?"

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse(
            "evaluation:assessment-detail",
            kwargs={"assessment_uuid": self.uuid},
        )

    def total_of_points(self):
        sum = 0
        for q in self.questioninfo_set.all():
            sum += q.point
        return sum

    def number_of_questions(self):
        return len(self.questions.all())

    total_of_points.short_description = "Total de Pontos"

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"


class QuestionInfo(models.Model):
    question = models.ForeignKey(
        Question, verbose_name="Questão", on_delete=models.CASCADE
    )

    assessment = models.ForeignKey(
        Assessment, verbose_name="Avaliação", on_delete=models.CASCADE
    )

    point = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Pontuação"
    )

    def __str__(self) -> str:
        return f"{self.assessment} - {self.question} - {self.point}"

    class Meta:
        verbose_name = "Questão da Avaliação"
        verbose_name_plural = "Questões da Avaliação"


class DateTimeRangeError(ValidationError):
    pass


def validate_submission_datetime(submission):
    assessment = submission.assessment
    assessment_begin_at = assessment.date_start
    assessment_end_at = assessment.date_end

    if submission.updated_at and submission.created_at:
        if (
            submission.updated_at < assessment_begin_at
            or submission.created_at > assessment_end_at
        ):
            raise DateTimeRangeError(
                f"AssessmentSubmission {submission.start_at} started outbound of Assessment {assessment_begin_at} - {assessment_end_at}"
            )


class AssessmentSubmission(models.Model):
    uuid = models.UUIDField(
        "uuid",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    assessment = models.ForeignKey(
        Assessment, verbose_name="Avaliação", on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        User,
        verbose_name="Autor",
        on_delete=models.CASCADE,
    )

    score = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Nota"
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Criado em"
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Atulizado em"
    )

    def __str__(self) -> str:
        return f"{self.assessment} de {self.author.first_name} {self.author.last_name} ({self.author})"

    def clean(self):
        validate_submission_datetime(self)

    def compute_score(self):
        questions = self.assessment.questions.all()

        submissions = Submission.objects.filter(
            author=self.author,
            status="OK",
            question__in=questions,
            timestamp__gt=self.assessment.date_start,
            timestamp__lt=self.assessment.date_end,
        )

        questions_id_with_submission_ok = list(
            submissions.values_list("question_id", flat=True)
        )

        questions_info_ok = self.assessment.questioninfo_set.filter(
            question_id__in=questions_id_with_submission_ok
        )

        points = 0
        for question_info in questions_info_ok:
            points += question_info.point

        self.score = points
        self.save()

        return points

    class Meta:
        verbose_name = "Avaliação do Aluno"
        verbose_name_plural = "Avaliações dos Alunos"
