# SaaS Salão de Beleza - Management Script
# Utilitário para inicializar dados básicos
# Execute com: python manage.py shell < init_data.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from servicos.models import Modulo

def criar_modulos():
    """Cria os módulos básicos se não existirem"""
    modulos_base = [
        {'nome': 'cabelo', 'descricao': 'Cortes e tratamentos capilares', 'icone': 'bi-scissors'},
        {'nome': 'pele', 'descricao': 'Maquiagem, tratamentos faciais e depilação', 'icone': 'bi-brush'},
        {'nome': 'unhas', 'descricao': 'Manicure e pedicure', 'icone': 'bi-palette'},
    ]
    
    for mod_data in modulos_base:
        modulo, created = Modulo.objects.get_or_create(
            nome=mod_data['nome'],
            defaults={
                'descricao': mod_data['descricao'],
                'icone': mod_data['icone']
            }
        )
        if created:
            print(f"✓ Módulo '{modulo}' criado com sucesso!")
        else:
            print(f"- Módulo '{modulo}' já existe.")

if __name__ == '__main__':
    print("Inicializando dados básicos...")
    criar_modulos()
    print("\n✅ Dados iniciais (módulos) criados com sucesso!")
    print("\nPróximos passos:")
    print("1. Inicie o servidor: python manage.py runserver")
    print("2. Acesse a página de cadastro para criar seu primeiro salão e usuário admin:")
    print("   http://127.0.0.1:8000/cadastro")
    print("3. (Opcional) Crie um superusuário global: python manage.py createsuperuser")
