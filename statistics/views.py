from session_security.views import PingView

from .domain import set_last_activity


class RecordLogPingView(PingView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if "_session_security" in request.session:
            ip = request.META.get("REMOTE_ADDR", "127.0.0.1")

            if "HTTP_X_FORWARDED_FOR" in request.META:
                ip = request.META.get("HTTP_X_FORWARDED_FOR", "")
                
            set_last_activity(request.user.username, ip)

        return response
