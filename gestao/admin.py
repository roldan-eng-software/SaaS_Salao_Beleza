from django.contrib import admin
from .models import Material, MovimentacaoEstoque, Transacao

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['nome', 'modulo', 'quantidade', 'unidade', 'estoque_minimo', 'estoque_baixo_display']
    list_filter = ['modulo']
    search_fields = ['nome', 'descricao']
    
    def estoque_baixo_display(self, obj):
        return '⚠️ Baixo' if obj.estoque_baixo else '✓ OK'
    estoque_baixo_display.short_description = 'Situação Estoque'

@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ['material', 'tipo', 'quantidade', 'usuario', 'criado_em']
    list_filter = ['tipo', 'criado_em']
    search_fields = ['material__nome', 'motivo']
    date_hierarchy = 'criado_em'

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'tipo', 'categoria', 'valor', 'data', 'pago']
    list_filter = ['tipo', 'categoria', 'pago', 'data']
    search_fields = ['descricao', 'observacoes']
    date_hierarchy = 'data'
    list_editable = ['pago']
    readonly_fields = ['criado_em', 'atualizado_em']
