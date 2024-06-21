from django.urls import path

from . import views

app_name = "evaluation"

urlpatterns = [
    path(
        "assessments/<str:assessment_uuid>",
        views.assessment_detail,
        name="assessment-detail",
    ),
]
