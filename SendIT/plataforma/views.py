from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Question, Submission, Tags, Perfil
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from random import randint
import logging

log = logging.getLogger(__name__)
log.setLevel(20)


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/home/")

    return render(request, "sistema/index.html")

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/home/")

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/home/')
    else:
        form = SignUpForm()
    return render(request, 'sistema/signup.html', {'form': form})

@login_required
def home(request):
    submissoes_ok = Submission.objects.filter(autor=request.user, status="OK")

    questions = Question.objects.exclude(submission__in=submissoes_ok)
    questions = questions.exclude(exibir=False)
    questions = questions.prefetch_related("tags")

    if "tag" in request.GET:
        tag = request.GET.get("tag")
        if tag != "all":
            questions = questions.filter(tags__tag__icontains=tag)

    questions = questions.order_by("xp")

    tags = Tags.objects.all()

    return render(
        request,
        "sistema/home.html",
        {"user": request.user, "questoes": questions, "tags": tags},
    )

@login_required
def random_question(request):
    q = Question.objects.exclude(exibir=False).order_by('?')[0]
    return HttpResponseRedirect(f'/question/{q.id}')


@login_required
def completed_issues(request):
    submissoes_ok = Submission.objects.filter(
        autor=request.user, status="OK"
    ).prefetch_related("questao")
    questions = Question.objects.filter(submission__in=submissoes_ok).prefetch_related(
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
        "sistema/questoes-concluidas.html",
        {"questoes": questions, "tags": tags},
    )

@login_required
def get_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id, exibir=True)

    last_submission = Submission.objects.filter(
        autor=request.user, questao_id=question.id
    ).first()

    return render(
        request,
        "sistema/detalhe-questao.html",
        {"questao": question, "ultima_submissao": last_submission},
    )

@require_POST
@login_required
def create_submission(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    code = request.POST["editor"]
    lang = request.POST["language"]

    try:
        get_submission = Submission.objects.get(
            autor=request.user, questao=question, status="OK"
        )

        if get_submission:
            return HttpResponseRedirect("/completed-issues/")  
