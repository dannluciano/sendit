from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from core.models import Submission
from evaluation.models import Assessment, AssessmentSubmission, QuestionInfo


@login_required
def assessment_detail(request, assessment_uuid):
    assessment = get_object_or_404(Assessment, uuid=assessment_uuid)
    assessment_submission = AssessmentSubmission.objects.filter(
        assessment=assessment, author=request.user
    ).first()
    context = {
        "assessment": assessment,
        "assessment_submission": assessment_submission,
    }

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

    questions = assessment.questions.all()

    submissions = Submission.objects.filter(
        author=request.user,
        status="OK",
        question__in=questions,
        timestamp__gt=assessment.date_start,
        timestamp__lt=assessment.date_end,
    )

    questions_id_with_submission_ok = list(
        submissions.values_list("question_id", flat=True)
    )

    questions_info_ok = assessment.questioninfo_set.filter(
        question_id__in=questions_id_with_submission_ok
    )

    context = {
        "assessment": assessment,
        "assessment_submission": assessment_submission,
        "questions_info": questions_info,
        "questions_info_ok": questions_info_ok,
    }

    print(context)

    return render(
        request, "evaluation/assessment-questions-list.html", context=context
    )
