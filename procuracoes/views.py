from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from .models import Procuracao
from .forms import ProcuracaoForm
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Q # Importe a classe Q para consultas complexas

# View da página inicial (já existente)
@login_required
def home(request):
    hoje = timezone.localdate()
    limite_30_dias = hoje + timedelta(days=30)
    limite_60_dias = hoje + timedelta(days=60)

    procuracoes = Procuracao.objects.filter(usuario=request.user).order_by('data_vencimento')

    vencidas = [p for p in procuracoes if p.data_vencimento < hoje]
    vencem_em_30_dias = [p for p in procuracoes if hoje <= p.data_vencimento <= limite_30_dias]
    vencem_em_60_dias = [p for p in procuracoes if limite_30_dias < p.data_vencimento <= limite_60_dias]
    outras_procuracoes = [p for p in procuracoes if p.data_vencimento > limite_60_dias]

    context = {
        'vencidas': vencidas,
        'vencem_em_30_dias': vencem_em_30_dias,
        'vencem_em_60_dias': vencem_em_60_dias,
        'outras_procuracoes': outras_procuracoes,
    }

    return render(request, 'procuracoes/home.html', context)

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