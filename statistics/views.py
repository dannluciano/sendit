from session_security.views import PingView
from django.shortcuts import render

from .domain import set_last_activity


class RecordLogPingView(PingView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if "_session_security" in request.session:
            set_last_activity(request.user.username)

        return response
