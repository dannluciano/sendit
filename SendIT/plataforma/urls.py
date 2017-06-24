from django.conf.urls import url
from plataforma import views

urlpatterns = [
    url(r'^$', views.index),
]