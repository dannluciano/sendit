from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from evaluation.models import Assessment


@login_required
def assessment_detail(request, assessment_uuid):
    assessment = get_object_or_404(Assessment, uuid=assessment_uuid)
    context = {"assessment": assessment}

    return render(request, "core/assessment-detail.html", context=context)
