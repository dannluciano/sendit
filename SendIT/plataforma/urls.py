from django.urls import include, path
from . import views

app_name = 'plataforma'

urlpatterns = [
    path('', views.index, name="index"),
    path('home/', views.home, name="home"),
    path('aleatoria/', views.aleatoria, name="aleatoria"),
    path('questoes-concluidas/', views.questoes_concluidas, name="questoes-concluidas"),
    path('questoes/<int:questao_id>/submeter/', views.criar_submissao, name='submeter'),
    path('questao/<int:questao_id>/', views.ver_questao, name="ver-questao"),
    path('cadastrar/', views.cadastrar_usuario, name="cadastrar"),
    path('entrar/', views.entrar, name="entrar"),
    path('sair/', views.sair, name="sair"),
    path('pontuacao/', views.quadro_de_medalhas, name="pontuacao"),
]
