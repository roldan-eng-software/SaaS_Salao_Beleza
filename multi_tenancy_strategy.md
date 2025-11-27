# Análise de Viabilidade: Multi-Tenancy (Múltiplos Clientes)

## Estado Atual
Atualmente, a aplicação **AppSalão** foi projetada como um sistema **Single-Tenant** (Inquilino Único). Isso significa que:
- Existe apenas uma configuração de salão (`ConfiguracaoSalao`).
- Os dados (Agendamentos, Serviços, Financeiro) não possuem vínculo com uma "Empresa" ou "Salão" específico, pois assume-se que todo o banco de dados pertence a um único dono.
- Não há isolamento de dados entre diferentes salões no nível do banco de dados atual.

## É possível implementar Row Level Security (RLS)?
**Sim, é totalmente possível**, mas exige uma refatoração estrutural na aplicação.

Para suportar múltiplos clientes (vários salões usando o mesmo sistema, mas cada um vendo apenas seus dados), precisamos transformar a aplicação em **Multi-Tenant**.

## Estratégia de Implementação

### 1. Criação do Modelo Tenant (Salão)
Criar um modelo que represente a "Empresa" ou "Salão".
```python
class Salao(models.Model):
    nome = models.CharField(max_length=200)
    subdominio = models.CharField(max_length=100, unique=True) # ex: salao1.app.com
    # ... outros dados
```

### 2. Alteração nos Modelos Existentes
Todos os modelos que guardam dados específicos de um salão precisam de uma chave estrangeira para o modelo `Salao`.
- `Usuario` -> `Salao`
- `Servico` -> `Salao`
- `Agendamento` -> `Salao`
- `Transacao` -> `Salao`
- `Material` -> `Salao`

### 3. Implementação do "Row Level Security" (Isolamento Lógico)
No Django, isso é feito geralmente via **Managers Customizados** e **Middleware**.

#### Middleware
Intercepta a requisição, identifica qual é o salão (pelo subdomínio ou pelo usuário logado) e ativa o contexto do salão atual.

#### Custom Manager (O Segredo do RLS no Django)
Criamos um `Manager` que filtra automaticamente os dados com base no salão ativo.

```python
class TenantManager(models.Manager):
    def get_queryset(self):
        # Filtra automaticamente pelo salão do usuário logado/contexto atual
        return super().get_queryset().filter(salao=get_current_salao())
```

### 4. Adaptação das Views e Forms
- **Views**: Não precisam mudar muito se usarmos o Manager correto, mas na criação de objetos (`CreateView` ou `form.save()`), precisamos injetar o `salao_id` automaticamente.
- **Forms**: Precisam filtrar chaves estrangeiras (ex: ao agendar, mostrar apenas profissionais *daquele* salão).

## Conclusão
A aplicação suporta essa mudança. O esforço estimado seria de **médio a alto**, pois envolve:
1.  Criar o modelo de Salão.
2.  Migrar o banco de dados (adicionar colunas).
3.  Atualizar todas as queries para respeitar o isolamento.
4.  Ajustar o sistema de login/cadastro para vincular usuários a salões.
