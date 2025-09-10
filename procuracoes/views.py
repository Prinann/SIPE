from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from .models import Procuracao
from .forms import ProcuracaoForm
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def home(request):
    hoje = timezone.localdate()
    
    # Processa o formulário de cadastro se a requisição for POST
    if request.method == 'POST':
        form = ProcuracaoForm(request.POST)
        if form.is_valid():
            procuracao = form.save(commit=False)
            procuracao.usuario = request.user
            procuracao.save()
            return redirect(reverse('home')) # Redireciona para a mesma página
    else:
        form = ProcuracaoForm() # Cria um formulário vazio para requisições GET

    # Filtra as procurações para o usuário logado
    procuracoes = Procuracao.objects.filter(usuario=request.user).order_by('data_vencimento')
    
    total_procuracoes = procuracoes.count()
    vencidas = procuracoes.filter(data_vencimento__lt=hoje)
    vencem_em_30_dias = procuracoes.filter(data_vencimento__gte=hoje, data_vencimento__lte=hoje + timedelta(days=30))
    outras_procuracoes = procuracoes.filter(data_vencimento__gt=hoje + timedelta(days=30))

    context = {
        'form': form, # Adiciona o formulário ao contexto
        'total_procuracoes': total_procuracoes,
        'vencidas': vencidas,
        'vencem_em_30_dias': vencem_em_30_dias,
        'outras_procuracoes': outras_procuracoes,
    }
    
    return render(request, 'procuracoes/home.html', context)

def api_buscar_procuracoes(request):
    # ... (código da sua API de busca, não precisa mudar)
    pass

# ... (restante do seu código, como cadastrar_procuracao e api_buscar_procuracoes)

# View para o cadastro (já existente)
@login_required
def cadastrar_procuracao(request):
    if request.method == 'POST':
        form = ProcuracaoForm(request.POST)
        if form.is_valid():
            procuracao = form.save(commit=False)
            procuracao.usuario = request.user
            procuracao.save()
            return redirect(reverse('home'))
    else:
        form = ProcuracaoForm()

    return render(request, 'procuracoes/cadastrar_procuracao.html', {'form': form})

# Nova View para a API de busca
@login_required
def api_buscar_procuracoes(request):
    query = request.GET.get('q', '') # Pega o termo de busca da URL
    procuracoes = Procuracao.objects.filter(usuario=request.user)

    if query:
        # Filtra por outorgante ou outorgado, ignorando maiúsculas/minúsculas
        procuracoes = procuracoes.filter(
            Q(outorgante__icontains=query) | Q(outorgado__icontains=query)
        )

    # Converte os objetos para uma lista de dicionários
    lista_procuracoes = list(procuracoes.values('outorgante', 'outorgado', 'data_vencimento'))

    # Retorna a lista em formato JSON
    return JsonResponse({'procuracoes': lista_procuracoes})