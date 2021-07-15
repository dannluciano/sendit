from django.urls import path
from . import views

app_name = "editor"

urlpatterns = [
    path('', views.editor, name='editor'),
    path('runner/', views.create_runner, name='create_runner'),
    path('runner/<str:runner_uuid>/', views.runner_details, name='runner_details'),
]