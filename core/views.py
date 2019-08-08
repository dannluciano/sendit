from datetime import timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from .forms import SignUpForm
from .models import Question, Submission, Tags, UserData
from statistics.models import LeaderboardView
from .worker import run_submission_runner
import django_rq
import logging


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
    return UserData(request.user.id)


@login_required
def home(request):
    user = current_user_data(request)
    submissoes_ok = Submission.objects.filter(author=request.user, status="OK")
    questions = Question.objects.exclude(submission__in=submissoes_ok)
    questions = questions.exclude(visible=False)
    questions = questions.prefetch_related("tags")

    if "tag" in request.GET:
        tag = request.GET.get("tag")
        if tag != "all":
            questions = questions.filter(tags__tag__icontains=tag)

    questions = questions.order_by("xp")

    tags = Tags.objects.all()

    return render(
        request,
        "platform/home.html",
        {"user": user, "questions": questions, "tags": tags},
    )


@login_required
def random_question(request):
    q = Question.objects.exclude(visible=False).order_by("?")[0]
    return HttpResponseRedirect(f"/questions/{q.id}")


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

    return render(
        request,
        "platform/completed-questions.html",
        {"user": user, "questions": questions, "tags": tags},
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
        return HttpResponseRedirect("/completed-issues/")

    time_threshold = timezone.now() - timedelta(seconds=30)
    last_submissions = Submission.objects.filter(
        author=request.user, question=question, timestamp__gt=time_threshold
    )

    if last_submissions:
        log.info("Already exists Submission with less than 30 seconds")
        return HttpResponseRedirect(question.get_absolute_url())

    log.info("Does not exist any OK Submission")
    sub = Submission(author=request.user, question=question,
                     code=code, language=lang)
    sub.save()

    django_rq.enqueue(run_submission_runner, sub.id, ttl=60*60*24*7)
    log.info("Submission was to Queue")

    return HttpResponseRedirect("/submissions/")


@login_required
def medal_board(request):
    users = LeaderboardView.objects.order_by("-xp")
    return render(request, "platform/medal-board.html", {"users": users})


@login_required
def submissions_list(request):
    user = current_user_data(request)
    submissions = Submission.objects.select_related("question").filter(
        author=request.user
    )
    return render(
        request, "platform/submissions.html", {
            "submissions": submissions, "user": user}
    )
