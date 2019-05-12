from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from ckeditor.fields import RichTextField

import math
import random

from .submission_runner import SubmissionRunnerManager


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    xp = models.IntegerField(blank=True, default=0)

    @property
    def level(self):
        return int(math.sqrt(self.xp) * 1.5)

    @property
    def tx_conclusao(self):
        try:
            taxa = self.acertos / Question.objects.count() * 100.0
            return f'{taxa:5.2f}%'
        except ZeroDivisionError:
            return '-'

    @property
    def tx_sucesso(self):
        try:
            taxa = self.acertos / self.submissoes * 100.0
            return f'{taxa:5.2f}%'
        except ZeroDivisionError:
            return '-'

    @property
    def submissoes(self):
        return Submission.objects.filter(autor_id=self.user_id).count()

    @property
    def erros_de_sintax(self):
        return Submission.objects.filter(
            autor_id=self.user_id,
            status=Submission.STATUS_CHOICES[1][0]).count()

    @property
    def erros_de_execucao(self):
        return Submission.objects.filter(
            autor_id=self.user_id,
            status=Submission.STATUS_CHOICES[2][0]).count()

    @property
    def erros_de_tempo(self):
        return Submission.objects.filter(
            autor_id=self.user_id,
            status=Submission.STATUS_CHOICES[3][0]).count()

    @property
    def erros_de_saida(self):
        return Submission.objects.filter(
            autor_id=self.user_id,
            status=Submission.STATUS_CHOICES[4][0]).count()

    @property
    def acertos(self):
        return Submission.objects.filter(
            autor_id=self.user_id,
            status=Submission.STATUS_CHOICES[5][0]).count()

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['user__username']


@receiver(post_save, sender=User)
def criar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)


@receiver(post_save, sender=User)
def salvar_perfil(sender, instance, **kwargs):
    instance.perfil.save()


class Tags(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.tag}'

    class Meta:
        verbose_name_plural = 'Tags'
        verbose_name = 'Tags'


class Question(models.Model):
    titulo = models.CharField(max_length=255)
    enunciado = RichTextField()
    entrada = models.TextField(blank=True)
    saida = models.TextField(blank=True)
    xp = models.IntegerField(default=100)
    tags = models.ManyToManyField(Tags)
    exibir = models.BooleanField(default=True)

    def publish(self):
        self.save

    def __str__(self):
        return f'{self.titulo}'

    class Meta:
        ordering = ['titulo']


class CaseTest(models.Model):
    questao = models.ForeignKey(Question, on_delete=models.CASCADE)
    entrada = models.TextField(blank=True)
    saida = models.TextField(blank=True)

    def __str__(self):
        return f'Case - {self.id} : Questão: {self.questao}'


class Submission(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    questao = models.ForeignKey(Question, on_delete=models.CASCADE)
    codigo = models.TextField()
    STATUS_CHOICES = (
        ('Waiting', 'Esperando ser executada.'),
        ('SintaxError', 'Erro de sintaxe!'),
        ('RuntimeError', 'Erro em execução!'),
        ('TimeoutError', 'Tempo de execução excedido!'),
        ('DiffError', 'Saída computada diferente da saída esperada!'),
        ('OK', 'OK'))
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=36, default=STATUS_CHOICES[0])
    timestamp = models.DateTimeField(auto_now=True)

    LANGUAGE_CHOICES = (
        ('unkwon', 'Unkwon'),
        ('c', 'C'),
        ('c++11', 'C++11'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('python', 'Python'),
    )
    language = models.CharField(choices=LANGUAGE_CHOICES,
                              max_length=10, default=STATUS_CHOICES[0])

    STATUS_PHRASES = {
        'SintaxError': [
            ('Erro de sintaxe! Tente Novamente.', 'img/errosintaxe1.png'),
            ('Erro de sintaxe! Verifique os parenteses, colchetes e chaves.', 'img/errosintaxe2.png'),
            ('Ahhh não! Não consegui executar o seu código todo. Isso aconteceu por conta de um erro de sintaxe', 'img/errosintaxe3.png'),
            ('Será que não tem um ponto e vírgula ou um parênteses faltando?', 'img/errosintaxe4.png')
        ],
        'RuntimeError': [
            ('Erro de execução! Tente Novamente.', 'img/erroexecucao1.png'),
            ('Seu código morreu huahuahua! Ocorreu um erro de execução.', 'img/erroexecucao2.png'),
            ('Quando isso me acontece dá uma tristeza! Não consegiu executar o seu código. Tem alguma coisa erra nele.', 'img/erroexecucao3.png'),
            ('Tem certeza que não escreveu alguma nome errado? ', 'img/erroexecucao4.png')
        ],
        'TimeoutError': [
            ('Tempo de execução excedido! Me deu até sono! Tente Novamente.', 'img/tempoexecucao1.png'),
            ('O tempo pra executar esse código demorou tanto que eu já encontrei até um alienígena perdido! Tente Novamente.', 'img/tempoexecucao2.png'),
            ('Sabe a piadinha de navagadores? Seu código está abaixo do IE kkkkkkk', 'img/tempoexecucao3.png'),
            ('Até o Rubinho faria em um tempo melhor', 'img/tempoexecucao4.png')
        ],
        'DiffError': [
            ('Saída computada diferente da saída esperada!', 'img/differror1.png'),
            ('Essa foi por Pouco!', 'img/differror2.png'),
            ('Ops, esse código não era bem o que eu estava esperando!', 'img/differror3.png'),
            ('Encontrei um erro! A sua saída não está de acordo com a questão.', 'img/differror4.png')
        ],
        'OK': [
            ('Uau! Bem na mosca.', 'img/ok1.png'),
            ('Você não tem bola de cristal aí não né? Acertou tudo!', 'img/ok2.png'),
            ('Estou fascinado com essa solução. Parabéns', 'img/ok3.png'),
            ('Que coisa linda de se ver! Continue sempre assim.', 'img/ok4.png'),
            ('Que ideia brilhante, estou orgulhoso de você. Acertou a questão.', 'img/ok5.png')
        ]
    }

    def _get_random_status(self):
        try:
            self._random_status
        except AttributeError:
            self._random_status = random.choice(self.STATUS_PHRASES[self.status])
        return self._random_status

    def get_random_status_phrase(self):
        return self._get_random_status()[0]

    def get_random_status_image(self):
        return self._get_random_status()[1]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        casos_de_testes = self.questao.casetest_set.all()
        for cs in casos_de_testes:
            work_dir = f'{self.id}/{cs.id}'
            self.status = SubmissionRunnerManager().exe(self.language, work_dir, cs.entrada, cs.saida, self.codigo)
            if self.status != 'OK':
                break
        
        super().save(*args, **kwargs)
        
    def is_ok(self):
        return self.status == 'OK'

    def __str__(self):
        return f'Questão-{self.questao.id}-Submissão-{self.id}-{self.status}'

    class Meta:
        ordering = ['-id']


@receiver(pre_delete, sender=Submission)
def remove_xp(sender, instance, **kwargs):
    if instance.status == 'OK':
            perfil = instance.autor.perfil
            perfil.xp = perfil.xp - instance.questao.xp
            perfil.save()


class SubmissionSummary(models.Model):
    status = models.CharField(primary_key=True,
                              choices=Submission.STATUS_CHOICES,
                              max_length=36,
                              default=Submission.STATUS_CHOICES[0])
    sum = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'plataforma_submission_summary'
        verbose_name = 'Summary of Submission'
        verbose_name_plural = 'Summary of Submissions'
