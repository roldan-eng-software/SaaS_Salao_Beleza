from django.urls import path
from . import views

urlpatterns = [
    path('', views.servicos_lista, name='servicos_lista'),
    path('agendar/<int:servico_id>/', views.agendar_servico, name='agendar_servico'),
    path('cancelar/<int:agendamento_id>/', views.cancelar_agendamento, name='cancelar_agendamento'),
]
