from django.db import models
from .businnes import run_submission


class Questoes(models.Model):
    titulo = models.CharField(max_length=255)
    enunciado = models.TextField()
    entrada = models.TextField(blank=True)
    saida = models.TextField()

    def publish(self):
        self.save

    def __str__(self):
        return f'{self.titulo}'


class Submissoes(models.Model):
    questao = models.ForeignKey(Questoes)
    codigo = models.TextField()
    status = models.TextField()

    def publish(self):
        self.save

    def save(self, *args, **kwargs):
        try:
            run_submission(self.codigo,
                           self.questao.entrada,
                           self.questao.saida)
            self.status = 'OK'
        except Exception as error:
            self.status = error

        super(Submissoes, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.questao}-submissao-{self.id}'
