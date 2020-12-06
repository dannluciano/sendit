from editor.views import editor
from django.conf import settings
from django.urls import include, path
from django.contrib import admin

admin.site.site_header = "SendIt Administração"
admin.site.site_title = "SendIt"
admin.site.index_title = "SendIt"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("editor/", include("editor.urls")),
    path("session_security/", include("statistics.urls")),
    path("explorer/", include("explorer.urls")),
    path('django-rq/', include('django_rq.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
