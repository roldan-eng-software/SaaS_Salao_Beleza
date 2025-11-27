from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('profissionais/', views.gestao_profissionais, name='gestao_profissionais'),
    path('servicos/', views.gestao_servicos, name='gestao_servicos'),
    path('estoque/', views.gestao_estoque, name='gestao_estoque'),
    path('financeiro/', views.gestao_financeiro, name='gestao_financeiro'),
]
