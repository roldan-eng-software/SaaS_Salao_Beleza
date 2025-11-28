from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.db import models
from datetime import date, timedelta
from servicos.models import Agendamento, Profissional, Servico
from .models import Material, Transacao, MovimentacaoEstoque
from .forms import MaterialForm, TransacaoForm, ProfissionalForm, ServicoForm

def is_admin(user):
    """Verifica se usuário é admin"""
    return user.is_staff or user.tipo == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Dashboard administrativo"""
    hoje = date.today()
    mes_atual = hoje.replace(day=1)
    
    # Estatísticas
    total_agendamentos_mes = Agendamento.objects.filter(
        data__gte=mes_atual
    ).count()
    
    agendamentos_hoje = Agendamento.objects.filter(data=hoje).count()
    
    # Financeiro do mês
    receitas_mes = Transacao.objects.filter(
        tipo='receita',
        data__gte=mes_atual,
        pago=True
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    despesas_mes = Transacao.objects.filter(
        tipo='despesa',
        data__gte=mes_atual,
        pago=True
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    saldo_mes = receitas_mes - despesas_mes
    
    saldo_class = 'success' if saldo_mes >= 0 else 'danger'
    
    # Materiais com estoque baixo
    materiais_baixo = Material.objects.filter(
        quantidade__lte=models.F('estoque_minimo')
    ).count()
   
    # Próximos agendamentos
    proximos_agendamentos = Agendamento.objects.filter(
        data__gte=hoje
    ).exclude(status='cancelado').select_related('servico', 'cliente', 'profissional').order_by('data', 'hora')[:10]
    
    context = {
        'total_agendamentos_mes': total_agendamentos_mes,
        'agendamentos_hoje': agendamentos_hoje,
        'receitas_mes': receitas_mes,
        'despesas_mes': despesas_mes,
        'saldo_mes': saldo_mes,
        'saldo_class': saldo_class,
        'materiais_baixo': materiais_baixo,
        'proximos_agendamentos': proximos_agendamentos,
        'today': hoje,
    }
    return render(request, 'gestao/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def gestao_profissionais(request):
    """Gestão de profissionais"""
    profissionais = Profissional.objects.all().order_by('usuario__first_name')
    
    if request.method == 'POST':
        form = ProfissionalForm(request.POST)
        if form.is_valid():
            # Cria o usuário primeiro
            from core.models import Usuario
            
            user_data = {
                'username': form.cleaned_data['username'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'tipo': 'profissional',
                'salao': request.salao
            }
            
            try:
                user = Usuario.objects.create_user(**user_data)
                user.set_password(form.cleaned_data['password'])
                user.save()
                
                # Cria o profissional vinculado
                profissional = form.save(commit=False)
                profissional.usuario = user
                profissional.salao = request.salao
                profissional.save()
                
                # Salva M2M (módulos)
                form.save_m2m()
                
                messages.success(request, 'Profissional cadastrado com sucesso!')
                return redirect('gestao_profissionais')
            except Exception as e:
                messages.error(request, f'Erro ao criar profissional: {str(e)}')
    else:
        form = ProfissionalForm()
    
    context = {
        'profissionais': profissionais,
        'form': form,
    }
    return render(request, 'gestao/profissionais.html', context)


@login_required
@user_passes_test(is_admin)
def gestao_servicos(request):
    """Gestão de serviços"""
    servicos = Servico.objects.all().order_by('modulo', 'nome')
    
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            servico = form.save(commit=False)
            servico.salao = request.salao
            servico.save()
            messages.success(request, 'Serviço cadastrado com sucesso!')
            return redirect('gestao_servicos')
    else:
        form = ServicoForm()
    
    context = {
        'servicos': servicos,
        'form': form,
    }
    return render(request, 'gestao/servicos.html', context)


@login_required
@user_passes_test(is_admin)
def gestao_estoque(request):
    """Gestão de estoque"""
    materiais = Material.objects.all().order_by('modulo', 'nome')
    
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.salao = request.salao
            material.save()
            messages.success(request, 'Material cadastrado com sucesso!')
            return redirect('gestao_estoque')
    else:
        form = MaterialForm()
    
    context = {
        'materiais': materiais,
        'form': form,
    }
    return render(request, 'gestao/estoque.html', context)


@login_required
@user_passes_test(is_admin)
def gestao_financeiro(request):
    """Gestão financeira"""
    transacoes = Transacao.objects.all().order_by('-data')[:50]
    
    # Totais
    total_receitas = Transacao.objects.filter(tipo='receita', pago=True).aggregate(total=Sum('valor'))['total'] or 0
    total_despesas = Transacao.objects.filter(tipo='despesa', pago=True).aggregate(total=Sum('valor'))['total'] or 0
    saldo = total_receitas - total_despesas
    saldo_class = 'success' if saldo >= 0 else 'danger'
    
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.salao = request.salao
            transacao.save()
            messages.success(request, 'Transação registrada com sucesso!')
            return redirect('gestao_financeiro')
    else:
        form = TransacaoForm()
    
    context = {
        'transacoes': transacoes,
        'form': form,
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
        'saldo_class': saldo_class,
    }
    return render(request, 'gestao/financeiro.html', context)
