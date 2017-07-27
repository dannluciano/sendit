from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Question, Submission
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
    questoes = Question.objects.all()
    return render(request, 'sistema/home.html', {'questoes': questoes})


@login_required
def ver_questao(request, questao_id):
    questaoEscolhida = Question.objects.filter(id=questao_id)
    return render(request, 'sistema/detalhe-questao.html', {'questao': questaoEscolhida})


@require_POST
@login_required
def criar_submissao(request, questao_id):
    questao_id = questao_id
    questao = get_object_or_404(Question, pk=questao_id)
    questaoEnviada = Question.objects.all().filter(id=questao_id)
    xp_questao = questao.xp
    codigo = request.POST['editor']
    id_autor = request.user

    sub = Submission(autor=id_autor, questao=questao, codigo=codigo)
    sub.save()
    resultado = sub.status

    if resultado == 'OK':
        request.user.perfil.xp += xp_questao
        request.user.save()

    return render(request, 'sistema/resultado.html', {'codigo': codigo,
                                                      'questao': questaoEnviada,
                                                      'status': resultado,
                                                      'id_questao': questao_id,
                                                      'xp_questao': xp_questao})


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
    usuario = authenticate(username=usuario_aux.username, password=request.POST["senha"])
    if usuario is not None:
        login(request, usuario)
        return HttpResponseRedirect('/home/')

    return HttpResponseRedirect('/')


@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect('/')
