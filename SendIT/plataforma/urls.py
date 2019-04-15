from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^home/$', views.home),
    url(r'^aleatoria/$', views.aleatoria),
    url(r'^questoes-concluidas/$', views.questoes_concluidas),
    url(r'^questoes/(?P<questao_id>\d+)/submeter/$',
        views.criar_submissao, name='criar_submissao'),
    url(r'^questao/(?P<questao_id>\d+)/$', views.ver_questao),
    url(r'^cadastrar/$', views.cadastrar_usuario),
    url(r'^entrar/$', views.entrar),
    url(r'^sair/$', views.sair)
]
