from django.conf import settings
from django.urls import include, path
from django.contrib import admin

admin.site.site_header = "SendIt Administração"
admin.site.site_title = "SendIt"
admin.site.index_title = "SendIt"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("plataforma.urls", namespace="plataforma")),
    path("session_security/", include("session_security.urls")),
    path("explorer/", include("explorer.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
