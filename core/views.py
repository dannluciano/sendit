import logging
from datetime import timedelta
from statistics.models import LeaderboardView

import django_rq
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .domain import get_best_users_of_week, random_unresolved_question
from .forms import SignUpForm
from .models import Achievement, Question, Submission, Tags, UserData
from .worker import run_submission_runner

log = logging.getLogger(__name__)
log.setLevel(20)


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/home/")

    return render(request, "platform/index.html")


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/home/")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect("/home/")
    else:
        form = SignUpForm()
    return render(request, "platform/signup.html", {"form": form})


def current_user_data(request):
    return UserData(request.user.id, request.user.username)


@login_required
def home(request):
    user = current_user_data(request)
    submissoes_ok = Submission.objects.filter(author=request.user, status="OK")
    questions = Question.objects.exclude(submission__in=submissoes_ok)
    questions = questions.exclude(visible=False)
    questions = questions.prefetch_related("tags")
    achievements = Achievement.objects.filter(
        users=request.user
    )

    if "tag" in request.GET:
        tag = request.GET.get("tag")
        if tag != "all":
            questions = questions.filter(tags__tag__icontains=tag)

    questions = questions.order_by("xp")[:10]

    tags = Tags.objects.all()

    best_users_of_week = get_best_users_of_week()

    return render(
        request,
        "platform/home.html",
        {
            "user": user,
            "questions": questions,
            "tags": tags,
            "best_users_of_week": best_users_of_week,
            "achievements": achievements,
        },
    )


@login_required
def random_question(request):
    q = random_unresolved_question(request.user)
    if q:
        return HttpResponseRedirect(f"/questions/{q.id}")
    else:
        return HttpResponseRedirect("/home/")


@login_required
def completed_issues(request):
    user = current_user_data(request)
    ok_submissions = Submission.objects.filter(
        author=request.user, status="OK"
    ).prefetch_related("question")
    questions = Question.objects.filter(submission__in=ok_submissions).prefetch_related(
        "tags"
    )

    tags = Tags.objects.distinct().filter(question__in=questions)

    if "tag" in request.GET:
        tag = request.GET.get("tag")
        if tag != "all":
            questions = questions.filter(tags__tag__icontains=tag)

    questions = questions.order_by("-id")

    best_users_of_week = get_best_users_of_week()

    return render(
        request,
        "platform/completed-questions.html",
        {
            "user": user,
            "ok_submissions": ok_submissions,
            "tags": tags,
            "best_users_of_week": best_users_of_week,
        },
    )


@login_required
def get_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id, visible=True)

    last_submission = Submission.objects.filter(
        author=request.user, question_id=question.id
    ).first()

    return render(
        request,
        "platform/detail-question.html",
        {"question": question, "last_submission": last_submission},
    )


@require_POST
@login_required
def create_submission(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    code = request.POST["editor"]
    lang = request.POST["language"]

    log.info("New Submission Received")

    ok_submission = Submission.objects.filter(
        author=request.user, question=question, status="OK"
    )
    if ok_submission:
        log.info("Already exists OK Submission")
        return HttpResponseRedirect(question.get_absolute_url())

    time_threshold = timezone.now() - timedelta(seconds=15)
    last_submissions = Submission.objects.filter(
        author=request.user, question=question, timestamp__gt=time_threshold
    )

    if last_submissions:
        log.info("Already exists Submission with less than 15 seconds")
        return HttpResponseRedirect(question.get_absolute_url())

    log.info("Does not exist any OK Submission")
    sub = Submission(author=request.user, question=question, code=code, language=lang)
    sub.save()

    ttl = 60 * 60 * 24 * 7
    django_rq.enqueue(run_submission_runner, sub.id, ttl=ttl, result_ttl=ttl)
    log.info("Submission was to Queue")

    return HttpResponseRedirect(sub.get_absolute_url())


@login_required
def medal_board(request):
    users = LeaderboardView.objects.order_by("-xp")

    current_group = request.GET.get("group", "all")
    if current_group != "all":
        users = users.filter(group=current_group)

    groups = Group.objects.filter(~Q(name="Staff")).order_by("-name")

    return render(
        request,
        "platform/medal-board.html",
        {
            "current_user": request.user.username,
            "current_group": current_group,
            "users": users,
            "groups": groups,
        },
    )


@login_required
def submissions_list(request):
    user = current_user_data(request)
    submissions = (
        Submission.objects.select_related("question")
        .filter(
            author=request.user,
        )
        .exclude(status="Waiting")
    )

    return render(
        request, "platform/submissions.html", {"submissions": submissions, "user": user}
    )


@login_required
def submission_detail(request, submission_uuid):
    submission = get_object_or_404(Submission, uuid=submission_uuid)

    if submission.author != request.user and request.user.is_staff is False:
        return HttpResponseRedirect("/home/")

    if submission.is_waiting:
        return HttpResponseRedirect(submission.get_absolute_url())

    return render(
        request, "platform/submission-detail.html", {"submission": submission}
    )


@login_required
def submission_status(request, submission_uuid):
    submission = get_object_or_404(Submission, uuid=submission_uuid)
    if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
        dict = {
            "uuid": submission.uuid,
            "status": submission.status,
            "url": submission.get_absolute_url(),
        }
        return JsonResponse(dict)
    else:
        return render(
            request, "platform/submission-status.html", {"submission": submission}
        )
