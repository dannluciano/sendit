from django.conf.urls import url
from plataforma import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^questoes/(?P<questao_id>\d+)/submeter/$',
        views.criar_submissao, name='criar_submissao'),
    url(r'^questao/(?P<questao_id>\d+)/$', views.verQuestao)
]
