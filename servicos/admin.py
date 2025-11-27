from django.contrib import admin
from .models import Modulo, Servico, Profissional, Agendamento

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ['get_nome_display', 'icone']
    search_fields = ['nome']

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'modulo', 'preco', 'duracao_minutos', 'ativo']
    list_filter = ['modulo', 'ativo']
    search_fields = ['nome', 'descricao']
    list_editable = ['preco', 'ativo']

@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'get_modulos', 'horario_inicio', 'horario_fim', 'ativo']
    list_filter = ['ativo', 'modulos']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'usuario__username']
    filter_horizontal = ['modulos']
    
    def get_modulos(self, obj):
        return ", ".join([str(m) for m in obj.modulos.all()])
    get_modulos.short_description = 'Módulos'

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'profissional', 'servico', 'data', 'hora', 'status']
    list_filter = ['status', 'data', 'servico__modulo']
    search_fields = ['cliente__first_name', 'cliente__last_name', 'profissional__usuario__first_name']
    date_hierarchy = 'data'
    list_editable = ['status']
    readonly_fields = ['criado_em', 'atualizado_em']
