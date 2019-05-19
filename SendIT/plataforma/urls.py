from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'plataforma'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='sistema/index.html', redirect_authenticated_user=True, redirect_field_name = '/home/'), name='index'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'),  name='sair'),
    path('home/', views.home, name="home"),
    path('random/', views.random_question, name="aleatoria"),
    path('completed-issues/', views.completed_issues, name="questoes-concluidas"),
    path('question/<int:question_id>/submit/', views.create_submission, name='submeter'),
    path('question/<int:question_id>/', views.get_question, name="ver-questao"),
    path('signup/', views.signup, name="cadastrar"),
    path('ranking/', views.medal_board, name="pontuacao"),
]
