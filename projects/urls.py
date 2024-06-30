from django.urls import path

from .views import home, project_detail, project_new

app_name = "projects"

urlpatterns = [
    path("", home, name="home"),
    path("projects/new", project_new, name="project-new"),
    path("<project_name>", project_detail, name="project-detail"),
]
