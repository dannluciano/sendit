from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Questoes, Submissoes


def index(request):
    questoes = Questoes.objects.all()
    return render(request, 'sistema/index.html', {'questoes':questoes})

def verQuestao(request, questao_id):
  questaoEscolhida = Questoes.objects.filter(id=questao_id)
  return render(request, 'sistema/ver-questao.html', {'questao': questaoEscolhida})

@require_POST
def criar_submissao(request, questao_id):
    questao = get_object_or_404(Questoes, pk=questao_id)
    questaoEnviada = Questoes.objects.all().filter(id=questao_id)
    codigo = request.POST['editor']

    sub = Submissoes(questao=questao, codigo=codigo)
    sub.save()

    return render(request, 'sistema/resultado.html', {'codigo': codigo, 'questao':questaoEnviada})
