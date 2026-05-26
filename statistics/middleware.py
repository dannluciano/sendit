from django.conf import settings

from .domain import set_last_activity


class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        status_200 = response.status_code == 200
        path_is_not_static = not request.path.startswith(settings.STATIC_URL)
        user_is_authenticated = request.user.is_authenticated

        ip = request.META.get("REMOTE_ADDR", "127.0.0.1")

        if "HTTP_X_FORWARDED_FOR" in request.META:
            ip = request.META.get("HTTP_X_FORWARDED_FOR", "")

        if status_200 and path_is_not_static and user_is_authenticated:
            set_last_activity(request.user.username, ip)

        return response
