from django.db import models
from django.conf import settings

from core.models import Salao
from core.utils import TenantManager

class Material(models.Model):
    """Controle de estoque de materiais"""
    MODULO_CHOICES = (
        ('cabelo', 'Cabelo'),
        ('pele', 'Pele'),
        ('unhas', 'Unhas'),
        ('geral', 'Geral'),
    )
    
    salao = models.ForeignKey(Salao, on_delete=models.CASCADE, related_name='materiais', verbose_name='Salão', null=True)
    nome = models.CharField('Nome do Material', max_length=200)
    modulo = models.CharField('Módulo', max_length=20, choices=MODULO_CHOICES)
    descricao = models.TextField('Descrição', blank=True)
    
    quantidade = models.DecimalField('Quantidade em Estoque', max_digits=10, decimal_places=2, default=0)
    unidade = models.CharField('Unidade', max_length=20, default='unidade')
    
    custo_unitario = models.DecimalField('Custo Unitário', max_digits=10, decimal_places=2, default=0)
    estoque_minimo = models.DecimalField('Estoque Mínimo', max_digits=10, decimal_places=2, default=10)
    
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    objects = TenantManager()
    
    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'
        ordering = ['modulo', 'nome']
    
    def __str__(self):
        return f"{self.nome} ({self.get_modulo_display()}) - {self.quantidade} {self.unidade}"
    
    @property
    def estoque_baixo(self):
        """Verifica se está com estoque baixo"""
        return self.quantidade <= self.estoque_minimo


class MovimentacaoEstoque(models.Model):
    """Registro de movimentações de estoque"""
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('ajuste', 'Ajuste'),
    )
    
    salao = models.ForeignKey(Salao, on_delete=models.CASCADE, related_name='movimentacoes', verbose_name='Salão', null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='Material', related_name='movimentacoes')
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES)
    quantidade = models.DecimalField('Quantidade', max_digits=10, decimal_places=2)
    motivo = models.CharField('Motivo', max_length=500, blank=True)
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuário Responsável'
    )
    
    criado_em = models.DateTimeField('Data', auto_now_add=True)
    
    objects = TenantManager()
    
    class Meta:
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Movimentações de Estoque'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.material.nome} - {self.quantidade}"


class Transacao(models.Model):
    """Controle financeiro - receitas e despesas"""
    TIPO_CHOICES = (
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    )
    
    CATEGORIA_CHOICES = (
        ('servico', 'Serviço Prestado'),
        ('fornecedor', 'Fornecedor'),
        ('salario', 'Salário'),
        ('aluguel', 'Aluguel'),
        ('conta', 'Conta (Água, Luz, etc)'),
        ('outro', 'Outro'),
    )
    
    salao = models.ForeignKey(Salao, on_delete=models.CASCADE, related_name='transacoes', verbose_name='Salão', null=True)
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES)
    categoria = models.CharField('Categoria', max_length=30, choices=CATEGORIA_CHOICES)
    descricao = models.CharField('Descrição', max_length=500)
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    
    data = models.DateField('Data')
    pago = models.BooleanField('Pago/Recebido', default=False)
    
    # Relacionamentos opcionais
    agendamento = models.ForeignKey(
        'servicos.Agendamento',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Agendamento Relacionado',
        related_name='transacoes'
    )
    
    profissional = models.ForeignKey(
        'servicos.Profissional',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Profissional',
        related_name='transacoes'
    )
    
    observacoes = models.TextField('Observações', blank=True)
    
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    objects = TenantManager()
    
    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-data', '-criado_em']
    
    def __str__(self):
        sinal = '+' if self.tipo == 'receita' else '-'
        return f"{sinal} R$ {self.valor} - {self.descricao} ({self.data})"
