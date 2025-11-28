from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Salao

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'tipo', 'salao', 'is_staff')
    list_filter = ('tipo', 'is_staff', 'is_active', 'salao')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações do Salão', {'fields': ('salao',)}),
        ('Informações Adicionais', {'fields': ('cpf', 'telefone', 'tipo', 'foto')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações do Salão', {'fields': ('salao',)}),
        ('Informações Adicionais', {'fields': ('cpf', 'telefone', 'tipo')}),
    )

@admin.register(Salao)
class SalaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'subdominio', 'ativo', 'criado_em')
    search_fields = ('nome', 'subdominio')
    list_filter = ('ativo',)
    
    fieldsets = (
        (None, {'fields': ('nome', 'subdominio', 'logo', 'ativo')}),
        ('Contato e Endereço', {'fields': ('telefone', 'email', 'endereco')}),
        ('Módulos Ativos', {'fields': ('modulo_cabelo', 'modulo_pele', 'modulo_unhas')}),
    )
