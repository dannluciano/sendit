import random
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

from .utils import raw_sql

User._meta.get_field("email")._unique = True


class UserData:
    def __init__(self, _id, _username, *args, **kwargs):
        self.id = _id
        self.username = _username
        self.cache = None
        self.setup_cache()

    def setup_cache(self):
        SQL = """
                SELECT t1.*, t2.* FROM
                (SELECT SUM(check_out - check_in) as time FROM statistics_logrecord WHERE statistics_logrecord.user = %s) as t1,
                (SELECT 
                	auth_user.username as username
                    , auth_user.first_name as first_name
                    , auth_user.last_name as last_name
                    , coalesce(SUM(core_question.xp) FILTER (WHERE status='OK'), 0) AS xp
                    , LEAST(coalesce(sqrt(SUM(core_question.xp) FILTER (WHERE status='OK')) * 1.5, 0, 74))::int as level
                    , COUNT(core_question.id) FILTER (WHERE status='OK') AS OK
                    , COUNT(core_question.id) FILTER (WHERE status!='OK') AS NOT_OK
                FROM core_submission
                JOIN core_question ON (core_submission.question_id = core_question.id)
                RIGHT JOIN auth_user ON (core_submission.author_id = auth_user.id)
                WHERE auth_user.id = %s
                GROUP BY auth_user.username, auth_user.first_name, auth_user.last_name) as t2
        """
        self.cache = raw_sql(SQL, [self.username, self.id])

    def username(self):
        return self.username

    def level(self):
        return self.cache[0].level

    def xp(self):
        axp = Achievement.objects.filter(users=self.id).aggregate(Sum("xp"))
        if axp["xp__sum"]:
            return self.cache[0].xp + axp["xp__sum"]
        return self.cache[0].xp

    def ok(self):
        return self.cache[0].ok

    def not_ok(self):
        return self.cache[0].not_ok

    def full_name(self):
        fn = self.cache[0].first_name
        ln = self.cache[0].last_name

        return f"{fn} {ln}"

    def total_time_on(self):
        return self.cache[0].time

    def avatar_url(self):
        level = self.level()
        return f"img/platform/levels/level_{level}.png"


class Tags(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tag}"

    class Meta:
        verbose_name_plural = "Tags"
        verbose_name = "Tags"


class Question(models.Model):
    title = models.CharField(max_length=255)
    statement = CKEditor5Field(config_name="extends")
    sample_input = models.TextField(blank=True)
    sample_output = models.TextField(blank=True)
    xp = models.IntegerField(default=100)
    tags = models.ManyToManyField(Tags)
    visible = models.BooleanField(default=True)
    uuid = models.UUIDField(
        "uuid",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    def get_absolute_url(self):
        return reverse(
            "core:question_detail_by_uuid",
            args=[
                self.uuid,
            ],
        )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ["title"]


class CaseTest(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    sample_input = models.TextField(blank=True)
    sample_output = models.TextField(blank=True)

    def __str__(self):
        return f"Case - {self.id} : Questão: {self.question}"


class Submission(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_submission"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code = models.TextField()
    STATUS_CHOICES = (
        ("Waiting", "Esperando ser executada."),
        ("SintaxError", "Erro de sintaxe!"),
        ("RuntimeError", "Erro em execução!"),
        ("TimeoutError", "Tempo de execução excedido!"),
        ("DiffError", "Saída computada diferente da saída esperada!"),
        ("OK", "OK"),
    )
    status = models.CharField(
        choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0], max_length=255
    )
    timestamp = models.DateTimeField(auto_now=True)

    LANGUAGE_CHOICES = (
        ("unkwon", "Unkwon"),
        ("c", "C"),
        ("cplusplus", "C++"),
        ("javascript", "JavaScript"),
        ("java", "Java"),
        ("python", "Python"),
    )
    language = models.CharField(
        choices=LANGUAGE_CHOICES,
        max_length=10,
        default=LANGUAGE_CHOICES[0][0],
    )

    log = models.TextField(blank=True)
    output = models.TextField(blank=True)

    STATUS_PHRASES = {
        "SintaxError": [
            ("Erro de sintaxe! Tente Novamente.", "img/errosintaxe1.png"),
            (
                "Erro de sintaxe! Verifique os parenteses, colchetes e chaves.",
                "img/errosintaxe2.png",
            ),
            (
                "Ahhh não! Não consegui executar o seu código todo. Isso aconteceu por conta de um erro de sintaxe",
                "img/errosintaxe3.png",
            ),
            (
                "Será que não tem um ponto e vírgula ou um parênteses faltando?",
                "img/errosintaxe4.png",
            ),
        ],
        "RuntimeError": [
            ("Erro de execução! Tente Novamente.", "img/erroexecucao1.png"),
            (
                "Seu código morreu huahuahua! Ocorreu um erro de execução.",
                "img/erroexecucao2.png",
            ),
            (
                "Quando isso me acontece dá uma tristeza! Não consegiu executar o seu código. Tem alguma coisa erra nele.",
                "img/erroexecucao3.png",
            ),
            (
                "Tem certeza que não escreveu alguma nome errado? ",
                "img/erroexecucao4.png",
            ),
        ],
        "TimeoutError": [
            (
                "Tempo de execução excedido! Me deu até sono! Tente Novamente.",
                "img/tempoexecucao1.png",
            ),
            (
                "O tempo pra executar esse código demorou tanto que eu já encontrei até um alienígena perdido! Tente Novamente.",
                "img/tempoexecucao2.png",
            ),
            (
                "Sabe a piadinha de navagadores? Seu código está abaixo do IE kkkkkkk",
                "img/tempoexecucao3.png",
            ),
            (
                "Até o Rubinho faria em um tempo melhor",
                "img/tempoexecucao4.png",
            ),
        ],
        "DiffError": [
            (
                "Saída computada diferente da saída esperada!",
                "img/differror1.png",
            ),
            ("Essa foi por Pouco!", "img/differror2.png"),
            (
                "Ops, esse código não era bem o que eu estava esperando!",
                "img/differror3.png",
            ),
            (
                "Encontrei um erro! A sua saída não está de acordo com a questão.",
                "img/differror4.png",
            ),
        ],
        "OK": [
            ("Uau! Bem na mosca.", "img/ok1.png"),
            (
                "Você não tem bola de cristal aí não né? Acertou tudo!",
                "img/ok2.png",
            ),
            ("Estou fascinado com essa solução. Parabéns", "img/ok3.png"),
            (
                "Que coisa linda de se ver! Continue sempre assim.",
                "img/ok4.png",
            ),
            (
                "Que ideia brilhante, estou orgulhoso de você. Acertou a questão.",
                "img/ok5.png",
            ),
        ],
    }

    @property
    def is_waiting(self):
        return self.status == self.STATUS_CHOICES[0][0]

    def get_absolute_url(self):
        if self.is_waiting:
            return f"/submissions/{self.uuid}/status/"
        return f"/submissions/{self.uuid}/"

    def _get_random_status(self):
        try:
            self._random_status
        except AttributeError:
            self._random_status = random.choice(
                self.STATUS_PHRASES[self.status]
            )
        return self._random_status

    def get_random_status_phrase(self):
        return self._get_random_status()[0]

    def get_random_status_image(self):
        return self._get_random_status()[1]

    def is_ok(self):
        return self.status == "OK"

    def __str__(self):
        return f"Questão-{self.question.id}-Submissão-{self.id}-{self.status}"

    class Meta:
        ordering = ["-id"]


class AchievementPicture(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)


class Achievement(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")

    badge = models.ImageField(
        upload_to="core.AchievementPicture/bytes/filename/mimetype",
        verbose_name="Imagem da Medalha",
    )

    xp = models.IntegerField(default=100, verbose_name="Experiência")

    users = models.ManyToManyField(
        to=User, related_name="achievements", verbose_name="Usuário"
    )

    hidden = models.BooleanField(default=False, verbose_name="Escondida?")

    def __str__(self):
        return f"{self.name}: {self.xp} XP"

    class Meta:
        verbose_name = "Medalha"
        verbose_name_plural = "Medalhas"
        ordering = ("name",)
