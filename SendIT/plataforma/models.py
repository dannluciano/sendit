from django.db import models

# Create your models here.
class Questoes(models.Model):
  titulo = models.CharField(max_length=255)
  enunciado = models.TextField()
  entrada = models.TextField(blank=True)
  saida = models.TextField()

  def publish(self):
    self.save

  def __str__(self):
    return self.titulo

class Submissoes(models.Model):
  questao = models.ForeignKey(Questoes)
  codigo = models.TextField()
  status = models.TextField()

  def publish(self):
    self.save

  def __str__(self):
    return self.questao