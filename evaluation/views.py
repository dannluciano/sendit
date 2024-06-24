from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from evaluation.models import Assessment, AssessmentSubmission, QuestionInfo


@login_required
def assessment_detail(request, assessment_uuid):
    assessment = get_object_or_404(Assessment, uuid=assessment_uuid)
    context = {"assessment": assessment}

    return render(
        request, "evaluation/assessment-detail.html", context=context
    )


@login_required
def assessment_start(request, assessment_uuid):
    assessment = get_object_or_404(Assessment, uuid=assessment_uuid)
    assessment_submission, _ = AssessmentSubmission.objects.get_or_create(
        assessment=assessment, author=request.user, defaults={"score": 0}
    )

    return redirect(
        reverse(
            "evaluation:assement-submission-detail",
            args=[
                assessment_submission.uuid,
            ],
        )
    )


@login_required
def assessment_submission_detail(request, assessment_submission_uuid):
    assessment_submission = AssessmentSubmission.objects.get(
        uuid=assessment_submission_uuid
    )

    assessment = assessment_submission.assessment

    questions_info = QuestionInfo.objects.filter(assessment=assessment)

    context = {
        "assessment": assessment,
        "assessment_submission": assessment_submission,
        "questions_info": questions_info,
    }

    return render(
        request, "evaluation/assessment-questions-list.html", context=context
    )
