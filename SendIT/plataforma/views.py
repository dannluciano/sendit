from django.shortcuts import render
from .models import Submissoes
# Create your views here.
def index(request):
  if request.POST:
    codigo = request.POST['editor']
    return render(request, 'sistema/resultado.html', {'codigo':codigo})
    
  return render(request, 'sistema/index.html')