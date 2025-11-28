from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

from core.models import Salao
from core.utils import TenantManager

class Modulo(models.Model):
    """Módulos de serviços disponíveis"""
    TIPO_CHOICES = (
        ('cabelo', 'Cabelo'),
        ('pele', 'Pele'),
        ('unhas', 'Unhas'),
    )
    
    nome = models.CharField('Nome', max_length=50, choices=TIPO_CHOICES, unique=True)
    descricao = models.TextField('Descrição', blank=True)
    icone = models.CharField('Ícone (Bootstrap Icons)', max_length=50, default='bi-scissors')
    
    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
    
    def __str__(self):
        return self.get_nome_display()


class Servico(models.Model):
    """Serviços oferecidos pelo salão"""
    salao = models.ForeignKey(Salao, on_delete=models.CASCADE, related_name='servicos', verbose_name='Salão')
    nome = models.CharField('Nome do Serviço', max_length=200)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, verbose_name='Módulo', related_name='servicos')
    descricao = models.TextField('Descrição', blank=True)
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    duracao_minutos = models.IntegerField('Duração (minutos)', default=60)
    ativo = models.BooleanField('Ativo', default=True)
    
    objects = TenantManager()
    
    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['modulo', 'nome']
    
    def __str__(self):
        return f"{self.nome} ({self.modulo}) - R$ {self.preco}"


class Profissional(models.Model):
    """Perfil de profissional vinculado a usuário"""
    salao = models.ForeignKey(Salao, on_delete=models.CASCADE, related_name='profissionais', verbose_name='Salão')
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name='Usuário',
        related_name='perfil_profissional'
    )
    modulos = models.ManyToManyField(Modulo, verbose_name='Módulos que Atende', related_name='profissionais')
    biografia = models.TextField('Biografia', blank=True)
    especialidades = models.CharField('Especialidades', max_length=500, blank=True)
    
    # Horários de trabalho
    horario_inicio = models.TimeField('Horário de Início', default='09:00')
    horario_fim = models.TimeField('Horário de Fim', default='18:00')
    
    # Dias da semana (0=Segunda, 6=Domingo)
    trabalha_segunda = models.BooleanField('Segunda-feira', default=True)
    trabalha_terca = models.BooleanField('Terça-feira', default=True)
    trabalha_quarta = models.BooleanField('Quarta-feira', default=True)
    trabalha_quinta = models.BooleanField('Quinta-feira', default=True)
    trabalha_sexta = models.BooleanField('Sexta-feira', default=True)
    trabalha_sabado = models.BooleanField('Sábado', default=False)
    trabalha_domingo = models.BooleanField('Domingo', default=False)
    
    ativo = models.BooleanField('Ativo', default=True)
    
    objects = TenantManager()
    
    class Meta:
        verbose_name = 'Profissional'
        verbose_name_plural = 'Profissionais'
    
    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username
    
    def dias_trabalho(self):
        """Retorna lista de dias que trabalha (0-6)"""
        dias = []
        if self.trabalha_segunda: dias.append(0)
        if self.trabalha_terca: dias.append(1)
        if self.trabalha_quarta: dias.append(2)
        if self.trabalha_quinta: dias.append(3)
        if self.trabalha_sexta: dias.append(4)
        if self.trabalha_sabado: dias.append(5)
        if self.trabalha_domingo: dias.append(6)
        return dias


class Agendamento(models.Model):
    """Agendamentos de clientes"""
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    )
    
    salao = models.ForeignKey(Salao, on_delete=models.CASCADE, related_name='agendamentos', verbose_name='Salão')
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Cliente',
        related_name='agendamentos'
    )
    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.CASCADE,
        verbose_name='Profissional',
        related_name='agendamentos'
    )
    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
        verbose_name='Serviço',
        related_name='agendamentos'
    )
    
    data = models.DateField('Data')
    hora = models.TimeField('Hora')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pendente')
    
    observacoes = models.TextField('Observações', blank=True)
    
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    objects = TenantManager()
    
    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-data', '-hora']
        unique_together = ['profissional', 'data', 'hora']
    
    def __str__(self):
        return f"{self.cliente.get_full_name()} - {self.servico.nome} - {self.data} {self.hora}"
    
    def clean(self):
        """Validações customizadas"""
        # Verifica se o profissional trabalha nesse dia
        if hasattr(self, 'data') and hasattr(self, 'profissional'):
            dia_semana = self.data.weekday()
            if dia_semana not in self.profissional.dias_trabalho():
                raise ValidationError('Profissional não trabalha neste dia da semana.')
            
            # Verifica horário de trabalho
            if self.hora < self.profissional.horario_inicio or self.hora >= self.profissional.horario_fim:
                raise ValidationError(f'Horário fora do expediente do profissional ({self.profissional.horario_inicio} - {self.profissional.horario_fim}).')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
