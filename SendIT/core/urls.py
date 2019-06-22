from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

app_name = "core"

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='platform/index.html', redirect_authenticated_user=True, redirect_field_name = '/home/'), name='index'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'),  name='logout'),
    path('home/', views.home, name="home"),
    path('random/', views.random_question, name="random"),
    path('completed-issues/', views.completed_issues, name="completed-question"),
    path('question/<int:question_id>/submit/', views.create_submission, name='submit'),
    path('question/<int:question_id>/', views.get_question, name="get-question"),
    path('signup/', views.signup, name="signup"),
    path('ranking/', views.medal_board, name="ranking"),
    path('submissions/', views.submissions_list, name="submissions")
]
