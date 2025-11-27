from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta, time
from .models import Modulo, Servico, Profissional, Agendamento
from .forms import AgendamentoForm
from core.models import ConfiguracaoSalao

def servicos_lista(request):
    """Lista de serviços disponíveis"""
    config = ConfiguracaoSalao.get_config()
    
    # Filtra serviços ativos baseado nos módulos ativos
    servicos = Servico.objects.filter(ativo=True)
    
    if not config.modulo_cabelo:
        servicos = servicos.exclude(modulo__nome='cabelo')
    if not config.modulo_pele:
        servicos = servicos.exclude(modulo__nome='pele')
    if not config.modulo_unhas:
        servicos = servicos.exclude(modulo__nome='unhas')
    
    # Agrupa por módulo
    modulos = Modulo.objects.all()
    servicos_por_modulo = {}
    for modulo in modulos:
        servicos_modulo = servicos.filter(modulo=modulo)
        if servicos_modulo.exists():
            servicos_por_modulo[modulo] = servicos_modulo
    
    context = {
        'servicos_por_modulo': servicos_por_modulo,
        'config': config,
    }
    return render(request, 'servicos/servicos_lista.html', context)


@login_required
def agendar_servico(request, servico_id):
    """Página de agendamento de serviço"""
    servico = get_object_or_404(Servico, id=servico_id, ativo=True)
    
    # Profissionais que atendem esse módulo
    profissionais = Profissional.objects.filter(
        modulos=servico.modulo,
        ativo=True
    )
    
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, servico=servico)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.cliente = request.user
            agendamento.salao = request.salao
            agendamento.servico = servico
            agendamento.save()
            messages.success(request, 'Agendamento realizado com sucesso!')
            return redirect('meus_agendamentos')
    else:
        form = AgendamentoForm(servico=servico)
    
    context = {
        'servico': servico,
        'profissionais': profissionais,
        'form': form,
    }
    return render(request, 'servicos/agendar_servico.html', context)


@login_required
def cancelar_agendamento(request, agendamento_id):
    """Cancelar agendamento"""
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, cliente=request.user)
    
    if agendamento.status in ['pendente', 'confirmado']:
        agendamento.status = 'cancelado'
        agendamento.save()
        messages.success(request, 'Agendamento cancelado com sucesso.')
    else:
        messages.error(request, 'Este agendamento não pode ser cancelado.')
    
    return redirect('meus_agendamentos')
