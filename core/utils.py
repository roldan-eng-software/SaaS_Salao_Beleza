from django.db import models
from threading import local

_thread_locals = local()

def get_current_salao():
    """Retorna o salão atual do thread local storage"""
    return getattr(_thread_locals, 'salao', None)

def set_current_salao(salao):
    """Define o salão atual no thread local storage"""
    _thread_locals.salao = salao

class TenantManager(models.Manager):
    """Manager que filtra automaticamente pelo salão atual"""
    
    def get_queryset(self):
        queryset = super().get_queryset()
        salao = get_current_salao()
        
        if salao:
            return queryset.filter(salao=salao)
        
        return queryset
