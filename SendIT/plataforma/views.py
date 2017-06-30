from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Questoes, Submissoes


def index(request):
    if request.POST:
        codigo = request.POST['editor']
        return render(request, 'sistema/resultado.html', {'codigo': codigo})

    return render(request, 'sistema/index.html')


@require_POST
def criar_submissao(request, questao_id):
    questao = get_object_or_404(Questoes, pk=questao_id)
    codigo = request.POST['editor']

    sub = Submissoes(questao=questao, codigo=codigo)
    sub.save()

    return render(request, 'sistema/resultado.html', {'codigo': codigo})
