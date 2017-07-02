from django.db import models
from .businnes import run_submission


class Questoes(models.Model):
    titulo = models.CharField(max_length=255)
    enunciado = models.TextField()
    entrada = models.TextField(blank=True)
    saida = models.TextField()
    tags = models.CharField(max_length=255, default="laços")

    def publish(self):
        self.save

    def __str__(self):
        return f'{self.titulo}'


class Submissoes(models.Model):
    questao = models.ForeignKey(Questoes)
    codigo = models.TextField()
    STATUS_CHOICES = (
        ('Waiting',         'Esperando ser executada.'),
        ('JSSintaxError',   'Erro de sintaxe!'),
        ('JSRuntimeError',  'Erro em execução!'),
        ('JSTimeoutError',  'Tempo de execução excedido!'),
        ('DiffError',       'Saída computada diferente da saída esperada!'),
        ('OK',              'OK'))
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=36, default=STATUS_CHOICES[0])

    def publish(self):
        self.save

    def save(self, *args, **kwargs):
        self.status = run_submission(self.codigo,
                                     self.questao.entrada,
                                     self.questao.saida)

        super(Submissoes, self).save(*args, **kwargs)

    def __str__(self):
        return f'Questão-{self.questao.id}-Submissão-{self.id}-{self.status}'
