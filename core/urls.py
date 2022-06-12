from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

app_name = "core"

urlpatterns = [
    path(
        "",
        auth_views.LoginView.as_view(
            template_name="platform/index.html",
            redirect_authenticated_user=True,
            redirect_field_name="next",
        ),
        name="index",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("home/", views.home, name="home"),
    path("questions/random/", views.random_question, name="random"),
    path("questions/completed/", views.completed_issues, name="completed-question"),
    path("questions/<int:question_id>/submit/", views.create_submission, name="submit"),
    path("questions/<int:question_id>/", views.get_question, name="question_detail"),
    path("signup/", views.signup, name="signup"),
    path("ranking/", views.medal_board, name="ranking"),
    path("submissions/", views.submissions_list, name="submissions"),
    path(
        "submissions/<str:submission_uuid>/",
        views.submission_detail,
        name="submissions-detail",
    ),
    path(
        "submissions/<str:submission_uuid>/status/",
        views.submission_status,
        name="submissions-status",
    ),
]
