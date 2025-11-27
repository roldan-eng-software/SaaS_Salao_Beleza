# AppSalão - Sistema de Gestão para Salões de Beleza

Sistema web SaaS modular para gestão completa de salões de beleza, desenvolvido com Django e Bootstrap 5.

## 🎯 Funcionalidades

### Área do Cliente
- ✅ Cadastro e autenticação segura
- ✅ Visualização de serviços por módulo
- ✅ Agendamento online de serviços
- ✅ Histórico de agendamentos
- ✅ Cancelamento de agendamentos
- ✅ Perfil personalizável

### Área Administrativa
- ✅ Dashboard com estatísticas
- ✅ Gestão de profissionais
- ✅ Gestão de serviços
- ✅ Controle de estoque com alertas
- ✅ Gestão financeira (receitas e despesas)
- ✅ Calendar de agendamentos

### Módulos Opcionais
- 💇 **Cabelo**: Cortes e tratamentos
- 💅 **Unhas**: Manicure e pedicure
- 💄 **Pele**: Maquiagem, tratamentos e depilação

## 🛠️ Stack Tecnológico

- **Backend**: Django 5.x com Python 3.12
- **Frontend**: Bootstrap 5 + Django Crispy Forms
- **Database**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Imagens**: Pillow
- **Controle de Versão**: Git

## 📋 Pré-requisitos

- Python 3.12 ou superior
- Git
- Navegador web moderno

## 🚀 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/SaaS_Salao_Beleza.git
cd SaaS_Salao_Beleza
```

### 2. Crie e ative o ambiente virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute as migrações
```bash
python manage.py migrate
```

### 5. Crie um superusuário (admin)
```bash
python manage.py createsuperuser
```

### 6. Crie dados iniciais (módulos)
```bash
python manage.py shell
```

Dentro do shell:
```python
from servicos.models import Modulo
Modulo.objects.create(nome='cabelo', icone='bi-scissors')
Modulo.objects.create(nome='pele', icone='bi-brush')
Modulo.objects.create(nome='unhas', icone='bi-palette')
exit()
```

### 7. Inicie o servidor de desenvolvimento
```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

## 📂 Estrutura do Projeto

```
SaaS_Salao_Beleza/
├── config/              # Configurações do Django
├── core/                # App principal (autenticação, landing page)
├── servicos/            # Módulo de serviços e agendamentos
├── gestao/              # Módulo administrativo (estoque, financeiro)
├── templates/           # Templates HTML
├── static/              # Arquivos estáticos (CSS, JS, imagens)
├── media/               # Uploads de usuários
├── requirements.txt     # Dependências Python
└── manage.py            # CLI do Django
```

## 🗄️ Migração para PostgreSQL (Produção)

### 1. Instale o PostgreSQL
https://www.postgresql.org/download/

### 2. Crie um banco de dados
```sql
CREATE DATABASE salao_db;
CREATE USER salao_user WITH PASSWORD 'sua_senha_segura';
GRANT ALL PRIVILEGES ON DATABASE salao_db TO salao_user;
```

### 3. Atualize as configurações

Edite `config/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'salao_db',
        'USER': 'salao_user',
        'PASSWORD': 'sua_senha_segura',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 4. Execute as migrações
```bash
python manage.py migrate
python manage.py createsuperuser
```

## 🌐 Deploy (ProFreeHost ou outro)

### 1. Configurações para produção

Em `config/settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com', 'www.seu-dominio.com']
```

### 2. Colete arquivos estáticos
```bash
python manage.py collectstatic
```

### 3. Configure o servidor WSGI conforme a hospedagem

## 🎨 Personalização

### Alterar cores
Edite `static/css/style.css` e modifique as variáveis CSS:
```css
:root {
    --primary-color: #6f42c1;
    --secondary-color: #fd7e14;
}
```

### Configurar módulos ativos
Acesse: Django Admin → Configuração do Salão

## 📝 Licença

Este projeto está sob a licença MIT.

## 👥 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no GitHub.

---

Desenvolvido com ❤️ para profissionais de beleza
