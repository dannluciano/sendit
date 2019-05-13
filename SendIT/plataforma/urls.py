from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index),
    path('home/', views.home),
    path('aleatoria/', views.aleatoria),
    path('questoes-concluidas/', views.questoes_concluidas),
    path('questoes/<int:questao_id>/submeter/', views.criar_submissao, name='criar_submissao'),
    path('questao/<int:questao_id>/', views.ver_questao),
    path('cadastrar/', views.cadastrar_usuario),
    path('entrar/', views.entrar),
    path('sair/', views.sair),
    path('pontuacao/', views.quadro_de_medalhas),
]
