from django.contrib.auth.models import AbstractUser
from django.db import models

class Salao(models.Model):
    """Modelo Tenant - Representa um Salão/Empresa"""
    nome = models.CharField('Nome do Salão', max_length=200)
    subdominio = models.CharField('Subdomínio', max_length=100, unique=True, help_text='Identificador único na URL (ex: salao1)')
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
    
    salao = models.ForeignKey(Salao, on_delete=models.CASCADE, related_name='usuarios', verbose_name='Salão', null=True, blank=True)
    cpf = models.CharField('CPF', max_length=14, unique=True, blank=True, null=True)
    telefone = models.CharField('Telefone', max_length=15, blank=True)
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES, default='cliente')
    foto = models.ImageField('Foto', upload_to='usuarios/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_tipo_display()})"


class ConfiguracaoSalao(models.Model):
    """Configuração de módulos ativos no salão (Singleton)"""
    modulo_cabelo = models.BooleanField('Módulo Cabelo', default=True)
    modulo_pele = models.BooleanField('Módulo Pele', default=True)
    modulo_unhas = models.BooleanField('Módulo Unhas', default=True)
    
    nome_salao = models.CharField('Nome do Salão', max_length=200, default='Meu Salão')
    telefone_salao = models.CharField('Telefone', max_length=15, blank=True)
    email_salao = models.EmailField('Email', blank=True)
    endereco_salao = models.TextField('Endereço', blank=True)
    logo = models.ImageField('Logo', upload_to='salao/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Configuração do Salão'
        verbose_name_plural = 'Configuração do Salão'
    
    def save(self, *args, **kwargs):
        # Garante que só existe uma configuração
        if not self.pk and ConfiguracaoSalao.objects.exists():
            raise ValueError('Já existe uma configuração. Edite a existente.')
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_config(cls):
        """Retorna a configuração única, criando se necessário"""
        config, created = cls.objects.get_or_create(pk=1)
        return config
    
    def __str__(self):
        return f"Configuração - {self.nome_salao}"
