import uuid

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from core.models import Question


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

    date_end = models.DateTimeField("Data de Fim", auto_now=False, auto_now_add=False)

    description = RichTextField("Descrição")

    questions = models.ManyToManyField(
        Question, verbose_name="Questões", through="QuestionInfo"
    )

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("assessment_detail", kwargs={"uuid": self.uuid})

    @property
    def total_of_points(self):
        sum = 0
        for q in self.questioninfo_set.all():
            sum += q.point
        return sum

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
    point = models.PositiveIntegerField(verbose_name="Pontuação")


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

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atulizado em")

    def clean(self):
        validate_submission_datetime(self)

    class Meta:
        verbose_name = "Avaliação do Aluno"
        verbose_name_plural = "Avaliações dos Alunos"


class AssessmentSubmissionQuestionAnswer(models.Model):
    uuid = models.UUIDField(
        "uuid",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    assessment_submission = models.ForeignKey(
        AssessmentSubmission, verbose_name="Avaliação", on_delete=models.CASCADE
    )

    question_info = models.ForeignKey(
        QuestionInfo, verbose_name="Questão", on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atulizado em")

    class Meta:
        verbose_name = "Avaliações dos Alunos: Resposta"
