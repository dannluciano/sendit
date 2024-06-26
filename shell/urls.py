from django.urls import path

from .views import home

app_name = "shell"

urlpatterns = [
    path("", home, name="home"),
]
