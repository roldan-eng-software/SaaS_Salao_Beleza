from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, ConfiguracaoSalao

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'tipo', 'is_staff']
    list_filter = ['tipo', 'is_staff', 'is_active']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('cpf', 'telefone', 'tipo', 'foto')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('cpf', 'telefone', 'tipo')}),
    )

@admin.register(ConfiguracaoSalao)
class ConfiguracaoSalaoAdmin(admin.ModelAdmin):
    list_display = ['nome_salao', 'modulo_cabelo', 'modulo_pele', 'modulo_unhas']
    
    def has_add_permission(self, request):
        # Permite adicionar apenas se não existir configuração
        return not ConfiguracaoSalao.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Não permite deletar a configuração
        return False
