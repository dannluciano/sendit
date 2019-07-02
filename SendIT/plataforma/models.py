from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse

from ckeditor.fields import RichTextField

import math
import random

from .utils import raw_sql


class UserData():
class UserData:
    def __init__(self, _id, *args, **kwargs):
        self.id = _id
        self.cache = None
        self.setup_cache()

    def setup_cache(self):
        SQL = """
                SELECT auth_user.username as username
                    , coalesce(SUM(plataforma_question.xp) FILTER (WHERE status='OK'), 0) AS xp
                    , LEAST(coalesce(sqrt(SUM(plataforma_question.xp) FILTER (WHERE status='OK')) * 1.5, 0, 74))::int as level
                FROM plataforma_submission
                JOIN plataforma_question ON (plataforma_submission.questao_id = plataforma_question.id)
                JOIN auth_user ON (plataforma_submission.autor_id = auth_user.id)
                LEFT JOIN auth_user ON (plataforma_submission.autor_id = auth_user.id)
                WHERE auth_user.id = %s
                GROUP BY auth_user.username 
        """
        self.cache = raw_sql(SQL, [self.id])

    def username(self):
        return self.cache[0].username

    def level(self):
        return self.cache[0].level

    def xp(self):
        return self.cache[0].xp

    def avatar_url(self):
        level = self.level()
        return f'img/plataforma/levels/level_{level}.png'
        return f"img/plataforma/levels/level_{level}.png"


class Tags(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tag}"

    class Meta:
        verbose_name_plural = "Tags"
        verbose_name = "Tags"


class Question(models.Model):
    titulo = models.CharField(max_length=255)
    enunciado = RichTextField()
    entrada = models.TextField(blank=True)
    saida = models.TextField(blank=True)
    xp = models.IntegerField(default=100)
    tags = models.ManyToManyField(Tags)
    exibir = models.BooleanField(default=True)

    def get_absolute_url(self):
        return f"/question/{self.pk}/"

    def publish(self):
        self.save

    def __str__(self):
        return f"{self.titulo}"

    class Meta:
        ordering = ["titulo"]


class CaseTest(models.Model):
    questao = models.ForeignKey(Question, on_delete=models.CASCADE)
    entrada = models.TextField(blank=True)
    saida = models.TextField(blank=True)

    def __str__(self):
        return f"Case - {self.id} : Questão: {self.questao}"


class Submission(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    questao = models.ForeignKey(Question, on_delete=models.CASCADE)
    codigo = models.TextField()
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
        ("c++11", "C++11"),
        ("javascript", "JavaScript"),
        ("java", "Java"),
        ("python", "Python"),
    )
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=10, default=STATUS_CHOICES[0][0]
    )

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
            ("Até o Rubinho faria em um tempo melhor", "img/tempoexecucao4.png"),
        ],
        "DiffError": [
            ("Saída computada diferente da saída esperada!", "img/differror1.png"),
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
            ("Você não tem bola de cristal aí não né? Acertou tudo!", "img/ok2.png"),
            ("Estou fascinado com essa solução. Parabéns", "img/ok3.png"),
            ("Que coisa linda de se ver! Continue sempre assim.", "img/ok4.png"),
            (
                "Que ideia brilhante, estou orgulhoso de você. Acertou a questão.",
                "img/ok5.png",
            ),
        ],
    }

    def _get_random_status(self):
        try:
            self._random_status
        except AttributeError:
            self._random_status = random.choice(
                self.STATUS_PHRASES[self.status])
        return self._random_status

    def get_random_status_phrase(self):
        return self._get_random_status()[0]

    def get_random_status_image(self):
        return self._get_random_status()[1]

    def is_ok(self):
        return self.status == "OK"

    def __str__(self):
        return f"Questão-{self.questao.id}-Submissão-{self.id}-{self.status}"

    class Meta:
        ordering = ["-id"]
