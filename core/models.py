from django.contrib.auth.models import AbstractUser
from django.db import models

class Salao(models.Model):
    """Modelo Tenant - Representa um Salão/Empresa"""
    nome = models.CharField('Nome do Salão', max_length=200)
    subdominio = models.CharField('Subdomínio', max_length=100, unique=True, help_text='Identificador único na URL (ex: salao1)')
    
    # Contato e Endereço
    telefone = models.CharField('Telefone', max_length=15, blank=True)
    email = models.EmailField('Email', blank=True)
    endereco = models.TextField('Endereço', blank=True)
    logo = models.ImageField('Logo', upload_to='logos_salao/', blank=True, null=True)

    # Módulos Ativos
    modulo_cabelo = models.BooleanField('Módulo Cabelo', default=True)
    modulo_pele = models.BooleanField('Módulo Pele', default=True)
    modulo_unhas = models.BooleanField('Módulo Unhas', default=True)
    
    # Controle
    ativo = models.BooleanField('Ativo', default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Salão'
        verbose_name_plural = 'Salões'
        
    def __str__(self):
        return self.nome


class Usuario(AbstractUser):
    """Modelo customizado de usuário"""
    TIPO_CHOICES = (
        ('cliente', 'Cliente'),
        ('profissional', 'Profissional'),
        ('admin', 'Administrador'),
    )
    
    salao = models.ForeignKey(Salao, on_delete=models.CASCADE, related_name='usuarios', verbose_name='Salão')
    cpf = models.CharField('CPF', max_length=14, unique=True, blank=True, null=True)
    telefone = models.CharField('Telefone', max_length=15, blank=True)
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES, default='cliente')
    foto = models.ImageField('Foto', upload_to='usuarios/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_tipo_display()})"
