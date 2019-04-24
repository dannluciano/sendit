from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('plataforma.urls')),
    url(r'session_security/', include('session_security.urls')),
]
