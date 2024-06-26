from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

admin.site.site_header = "SendIt Administração"
admin.site.site_title = "SendIt"
admin.site.index_title = "SendIt"


urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("", include("evaluation.urls", namespace="evaluation")),
    path("editor/", include("editor.urls")),
    path("sh/", include("shell.urls")),
    path("session_security/", include("statistics.urls")),
    path("django-rq/", include("django_rq.urls")),
    path("admin/", admin.site.urls),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("uploads/", include("db_file_storage.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))
    ] + urlpatterns
