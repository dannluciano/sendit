try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url

from .views import RecordLogPingView

urlpatterns = [
    url(
        'ping/$',
        RecordLogPingView.as_view(),
        name='session_security_ping',
    )
]
