from django.urls import path

from .views import RecordLogPingView

urlpatterns = [
    path(
        "ping/",
        RecordLogPingView.as_view(),
        name="session_security_ping",
    )
]
