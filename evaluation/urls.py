from django.urls import path

from . import views

app_name = "evaluation"

urlpatterns = [
    path(
        "assessments/<str:assessment_uuid>",
        views.assessment_detail,
        name="assessment-detail",
    ),
    path(
        "assessments/<str:assessment_uuid>/start",
        views.assessment_start,
        name="assessment-start",
    ),
    path(
        "assessments/submission/<str:assessment_submission_uuid>",
        views.assessment_submission_detail,
        name="assement-submission-detail",
    ),
]
