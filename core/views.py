from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CadastroUsuarioForm, PerfilUsuarioForm
from servicos.models import Servico, Profissional, Agendamento
from core.models import ConfiguracaoSalao

def home(request):
    """Landing page"""
    config = ConfiguracaoSalao.get_config()
    
    # Serviços em destaque
    servicos_destaque = Servico.objects.filter(ativo=True)[:6]
    
    context = {
        'config': config,
        'servicos': servicos_destaque,
    }
    return render(request, 'core/home.html', context)


from core.models import ConfiguracaoSalao, Salao
from django.utils.text import slugify

def cadastro(request):
    """Cadastro de novo usuário e salão"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Cria um salão para o usuário
            # TODO: Em um cenário real, pediria o nome do salão no form
            nome_salao = f"Salão de {user.first_name}"
            subdominio = slugify(nome_salao) + "-" + str(user.username)
            
            salao = Salao.objects.create(
                nome=nome_salao,
                subdominio=subdominio
            )
            
            user.salao = salao
            user.tipo = 'admin' # Quem cadastra é admin do seu salão
            user.save()
            
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso! Seu salão foi criado.')
            return redirect('dashboard')
    else:
        form = CadastroUsuarioForm()
    
    return render(request, 'core/cadastro.html', {'form': form})


def login_view(request):
    """Login de usuário"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo(a), {user.get_full_name() or user.username}!')
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    """Logout"""
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('home')


@login_required
def dashboard(request):
    """Dashboard do usuário (cliente ou profissional)"""
    user = request.user
    
    if user.tipo == 'admin' or user.is_staff:
        return redirect('admin_dashboard')
    
    # Agendamentos do cliente
    agendamentos = Agendamento.objects.filter(cliente=user).order_by('-data', '-hora')[:10]
    
    # Contagem de agendamentos pendentes
    agendamentos_pendentes = Agendamento.objects.filter(cliente=user, status='pendente').count()
    
    context = {
        'agendamentos': agendamentos,
        'agendamentos_pendentes': agendamentos_pendentes,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def perfil(request):
    """Editar perfil do usuário"""
    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = PerfilUsuarioForm(instance=request.user)
    
    return render(request, 'core/perfil.html', {'form': form})


@login_required
def meus_agendamentos(request):
    """Lista de agendamentos do usuário"""
    agendamentos = Agendamento.objects.filter(cliente=request.user).order_by('-data', '-hora')
    
    return render(request, 'core/meus_agendamentos.html', {'agendamentos': agendamentos})
