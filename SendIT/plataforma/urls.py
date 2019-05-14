from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'plataforma'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='sistema/index.html', redirect_authenticated_user=True, redirect_field_name = '/home/'), name='index'),
    path('sair/', auth_views.LogoutView.as_view(next_page='/'),  name='sair'),
    path('home/', views.home, name="home"),
    path('aleatoria/', views.aleatoria, name="aleatoria"),
    path('questoes-concluidas/', views.questoes_concluidas, name="questoes-concluidas"),
    path('questoes/<int:question_id>/submeter/', views.criar_submissao, name='submeter'),
    path('questao/<int:question_id>/', views.ver_questao, name="ver-questao"),
    path('cadastrar/', views.cadastrar_usuario, name="cadastrar"),
    path('pontuacao/', views.quadro_de_medalhas, name="pontuacao"),
]
