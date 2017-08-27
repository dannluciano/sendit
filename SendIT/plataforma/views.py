from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Question, Submission, Tags
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/home/")

    return render(request, 'sistema/index.html')


@login_required
def home(request):
    questoes_submetidas = Submission.objects.filter(autor=request.user, status='OK')
    tags = Tags.objects.all()

    questoes = Question.objects

    if 'tag' in request.GET:
        tag = request.GET.get('tag')
        if tag != 'all':
            questoes = questoes.filter(tags__tag__icontains=tag)

    questoes = questoes.order_by('-id')

    for questao_submetida in questoes_submetidas:
        for questao in questoes:
            if questao.id == questao_submetida.questao.id:
                questoes = questoes.exclude(id=questao_submetida.questao.id)

    return render(request,
                  'sistema/home.html', {
                      'user': request.user,
                      'questoes': questoes,
                      'tags': tags,
                      'link': 1
                  })


@login_required
def questoes_concluidas(request):
    submissoes = Submission.objects.filter(autor=request.user, status='OK')
    tags = Tags.objects.all()

    if 'tag' in request.GET:
        tag = request.GET.get('tag')
        if tag != 'all':
            submissoes = submissoes.filter(questao__tags__tag__icontains=tag)

    submissoes = submissoes.order_by('-questao__id')

    return render(request,
                  'sistema/questoes-concluidas.html', {
                      'submissoes': submissoes,
                      'tags': tags,
                      'link': 2})


@login_required
def ver_questao(request, questao_id):
    # Para nao abrir as questoes que ja submeteu
    questaoEscolhida = Question.objects.filter(id=questao_id).first()
    questoesSubmetidas = Submission.objects.filter(autor=request.user, status='OK')

    for questao_submetida in questoesSubmetidas:
        if questao_submetida.questao.id == questao_id:
            return HttpResponseRedirect("/home/")

    return render(request, 'sistema/detalhe-questao.html', {'questao': questaoEscolhida})


@require_POST
@login_required
def criar_submissao(request, questao_id):
    questao = get_object_or_404(Question, pk=questao_id)
    codigo = request.POST['editor']

    sub = Submission(autor=request.user, questao=questao, codigo=codigo)
    sub.save()

    if sub.status == 'OK':
        request.user.perfil.xp += questao.xp
        request.user.save()

    return render(request,
                  'sistema/resultado.html', {
                      'submissao': sub,
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
    usuario = authenticate(username=usuario_aux.username, password=request.POST["senha"])
    if usuario is not None:
        login(request, usuario)
        return HttpResponseRedirect('/home/')

    return HttpResponseRedirect('/')


@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect('/')
