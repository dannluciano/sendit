from django.urls import path
from . import views

app_name = "editor"

urlpatterns = [
    path("", views.editor, name="editor"),
    path("save/", views.file_code_save, name="file-code-save"),
    path("files/", views.file_code_list, name="file-code-list"),
    path(
        "files/<str:file_code_uuid>/", views.file_code_detail, name="file-code-detail"
    ),
    path(
        "files/<str:file_code_uuid>/destroy/",
        views.file_code_destroy,
        name="file-code-destroy",
    ),
    path("runner/", views.create_runner, name="create-runner"),
    path("runner/<str:runner_uuid>/", views.runner_details, name="runner-details"),
]
