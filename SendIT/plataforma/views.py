from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Question, Submission, Tags
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from random import randint


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/home/")

    return render(request, 'sistema/index.html')


@login_required
def home(request):
    submissoes_ok = Submission.objects.filter(
        autor=request.user, status='OK')

    questoes = Question.objects.exclude(submission__in=submissoes_ok)
    questoes = questoes.exclude(exibir=False)
    questoes = questoes.prefetch_related('tags')

    if 'tag' in request.GET:
        tag = request.GET.get('tag')
        if tag != 'all':
            questoes = questoes.filter(tags__tag__icontains=tag)

    questoes = questoes.order_by('-id')

    tags = Tags.objects.all()

    return render(request,
                  'sistema/home.html', {
                      'user': request.user,
                      'questoes': questoes,
                      'tags': tags,
                      'link': 1
                  })


@login_required
def questoes_concluidas(request):
    submissoes_ok = Submission.objects.filter(
        autor=request.user, status='OK').prefetch_related('questao')
    questoes = Question.objects.filter(
        submission__in=submissoes_ok).prefetch_related('tags')

    tags = Tags.objects.distinct().filter(question__in=questoes)

    if 'tag' in request.GET:
        tag = request.GET.get('tag')
        if tag != 'all':
            questoes = questoes.filter(tags__tag__icontains=tag)

    questoes = questoes.order_by('-id')

    return render(request,
                  'sistema/questoes-concluidas.html', {
                      'questoes': questoes,
                      'tags': tags,
                      'link': 2})


@login_required
def ver_questao(request, questao_id):
    questao = get_object_or_404(Question, pk=questao_id)
    ultima_submissao = Submission.objects.filter(
        autor=request.user, questao_id=questao.id).first()

    return render(request,
                  'sistema/detalhe-questao.html', {
                      'questao': questao,
                      'ultima_submissao': ultima_submissao,
                  })


@require_POST
@login_required
def criar_submissao(request, questao_id):
    questao = get_object_or_404(Question, pk=questao_id)
    codigo = request.POST['editor']

    try:
        pegar_submissao = Submission.objects.get(autor=request.user, questao=questao, status='OK')
        
        if pegar_submissao:
            return HttpResponseRedirect("/questoes-concluidas/")  

    except Submission.DoesNotExist:
        sub = Submission(autor=request.user, questao=questao, codigo=codigo)
        sub.save()

        animacoes = ['bounce',
                     'bounceIn',
                     'bounceInDown',
                     'bounceInRight',
                     'bounceInLeft',
                     'bounceInUp',
                     'flash',
                     'fadeInDown',
                     'zoomIn',
                     'jackInTheBox',
                     'rollIn']

        animacao = randint(0, 10)

        if sub.status == 'OK':
            request.user.perfil.xp += questao.xp
            request.user.save()

        return render(request,
                      'sistema/resultado.html', {
                          'submissao': sub,
                          'codigo_enviado': codigo,
                          'animacao': animacoes[animacao],
                      })


@require_POST
def cadastrar_usuario(request):
    try:
        usuario_aux = User.objects.get(email=request.POST['email'])

        if usuario_aux:
            return render(request, 'sistema/index.html', {'erro': True})

    except User.DoesNotExist:
        usuario = request.POST['usuario']
        email = request.POST['email']
        senha = request.POST['senha']
        novoUsuario = User.objects.create_user(username=email,
                                               first_name=usuario,
                                               email=email,
                                               password=senha)
        novoUsuario.save()
        return render(request, 'sistema/index.html', {'resposta': True})


@require_POST
def entrar(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/home/")

    usuario_aux = User.objects.get(email=request.POST['email'])
    usuario = authenticate(username=usuario_aux.username,
                           password=request.POST["senha"])
    if usuario is not None:
        login(request, usuario)
        return HttpResponseRedirect('/home/')

    return HttpResponseRedirect('/')


@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect('/')
