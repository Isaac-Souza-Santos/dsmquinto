# API de Tarefas - CRUD Completo

Uma API REST simples para gerenciamento de tarefas, implementando todas as operações CRUD básicas.

## 🚀 Funcionalidades

- ✅ **Criar** tarefas (POST)
- 📋 **Listar** todas as tarefas (GET)
- 🔍 **Obter** tarefa específica (GET)
- ✏️ **Atualizar** tarefas (PUT)
- 🗑️ **Excluir** tarefas (DELETE)

## 🏗️ Estrutura do Projeto

```
dpm/
├── src/
│   ├── api/
│   │   └── app.py          # Configuração da aplicação Flask
│   ├── models/
│   │   ├── tarefa.py       # Modelos e banco de dados
│   │   └── usuario.py      # Modelo de usuário e autenticação
│   ├── routes/
│   │   ├── api.py          # Rotas da API
│   │   ├── auth.py         # Rotas de autenticação
│   │   └── usuarios.py     # Rotas de usuários
│   └── utils/
│       ├── helpers.py      # Utilitários
│       ├── permissions.py   # Sistema de permissões
│       ├── authorization_strategy.py  # Padrão Strategy
│       ├── auth_middleware.py          # Middleware de autenticação
│       └── role_middleware.py          # Middleware de autorização
├── main.py                 # Ponto de entrada
├── requirements.txt        # Dependências
├── examples_strategy.py    # Exemplos do padrão Strategy
└── tarefas.db             # Banco SQLite (criado automaticamente)
```

## 📋 Campos da Tarefa

- **titulo** (obrigatório): Título da tarefa
- **descricao** (opcional): Descrição detalhada
- **status**: "pendente" ou "concluida" (padrão: "pendente")
- **data_criacao**: Data de criação (automática)
- **data_atualizacao**: Data da última atualização (automática)

## 🔌 Rotas da API

### 1. Listar Tarefas

```
GET /tarefas
```

Retorna todas as tarefas cadastradas.

**Resposta:**

```json
{
  "tarefas": [
    {
      "id": 1,
      "titulo": "Estudar Python",
      "descricao": "Revisar conceitos básicos",
      "status": "pendente",
      "data_criacao": "2024-01-15T10:30:00",
      "data_atualizacao": "2024-01-15T10:30:00"
    }
  ],
  "total": 1
}
```

### 2. Criar Tarefa

```
POST /tarefas
```

**Corpo da requisição:**

```json
{
  "titulo": "Nova Tarefa",
  "descricao": "Descrição da tarefa",
  "status": "pendente"
}
```

**Resposta (201):**

```json
{
  "id": 2,
  "titulo": "Nova Tarefa",
  "descricao": "Descrição da tarefa",
  "status": "pendente",
  "data_criacao": "2024-01-15T10:35:00",
  "data_atualizacao": "2024-01-15T10:35:00"
}
```

### 3. Obter Tarefa

```
GET /tarefas/{id}
```

Retorna uma tarefa específica por ID.

### 4. Atualizar Tarefa

```
PUT /tarefas/{id}
```

**Corpo da requisição:**

```json
{
  "titulo": "Título Atualizado",
  "status": "concluida"
}
```

### 5. Excluir Tarefa

```
DELETE /tarefas/{id}
```

**Resposta:**

```json
{
  "message": "Tarefa com ID 1 removida com sucesso",
  "status": "sucesso"
}
```

## 🛠️ Instalação e Uso

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a API

```bash
python main.py
```

### 3. Acessar a documentação

- **API**: http://localhost:5000
- **Swagger**: http://localhost:5000/docs

## 🗄️ Banco de Dados

- **SQLite**: Banco de dados simples e automático
- **Tabela**: `tarefas` criada automaticamente
- **Persistência**: Dados mantidos entre execuções

## 📚 Documentação Swagger

A API inclui documentação automática via Swagger UI, acessível em `/docs`. Inclui:

- Descrição de todas as rotas
- Modelos de dados
- Exemplos de requisição/resposta
- Códigos de status HTTP
- Interface para testar a API

## 🧪 Testando a API

### Com cURL

```bash
# Listar tarefas
curl http://localhost:5000/tarefas

# Criar tarefa
curl -X POST http://localhost:5000/tarefas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Teste", "descricao": "Tarefa de teste"}'

# Obter tarefa
curl http://localhost:5000/tarefas/1

# Atualizar tarefa
curl -X PUT http://localhost:5000/tarefas/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "concluida"}'

# Excluir tarefa
curl -X DELETE http://localhost:5000/tarefas/1
```

### Com Swagger UI

1. Acesse http://localhost:5000/docs
2. Use a interface interativa para testar todas as rotas
3. Visualize os modelos de dados e respostas

## 🔧 Tecnologias Utilizadas

- **Flask**: Framework web Python
- **Flask-RESTX**: Extensão para APIs REST com Swagger
- **SQLite**: Banco de dados embutido
- **Python**: Linguagem de programação

## 🎯 Design Patterns Implementados

### Categorias de Design Patterns

Os Design Patterns são organizados em 3 categorias principais:

1. **Criacionais (Creational)** - Como objetos são criados

   - Singleton, Factory Method, Abstract Factory, Builder, Prototype

2. **Estruturais (Structural)** - Como objetos e classes se organizam

   - Adapter, Facade, Decorator, Proxy, Composite, Bridge

3. **Comportamentais (Behavioral)** - Como objetos interagem e se comunicam
   - Observer, Strategy, Command, State, Chain of Responsibility, Mediator, Template Method, Iterator, Memento

### Strategy Pattern (Padrão Estratégia)

**Categoria:** Comportamental (Behavioral Pattern)

O projeto implementa o **padrão Strategy** para o sistema de autorização e permissões. Este padrão comportamental permite definir diferentes estratégias de autorização para cada nível de acesso, permitindo que o algoritmo de autorização varie independentemente dos clientes que o utilizam.

#### Estrutura

```
AuthorizationStrategy (Interface)
├── VisualizacaoStrategy    → Apenas leitura
├── GerencialStrategy       → Gerenciar tarefas e usuários
└── AdministrativoStrategy  → Acesso total
```

#### Arquivos

- `src/utils/authorization_strategy.py` - Implementação do padrão Strategy
- `src/utils/permissions.py` - Usa Strategy internamente
- `examples_strategy.py` - Exemplos de uso

#### Como Funciona

1. Cada nível de acesso possui sua própria estratégia
2. O `AuthorizationContext` seleciona a estratégia apropriada
3. As rotas usam `@require_permission()` que internamente usa Strategy
4. Fácil adicionar novos níveis sem modificar código existente

#### Exemplo de Uso

```python
from src.utils.authorization_strategy import create_authorization_context

# Criar contexto para usuário gerencial
context = create_authorization_context('gerencial')

# Verificar permissão
pode_criar = context.can_perform_action('tarefas:create')  # True
pode_admin = context.can_perform_action('system:admin')      # False

# Obter todas as permissões
permissoes = context.get_allowed_actions()
```

#### Benefícios

- Código isolado e testável
- Fácil manutenção e extensão
- Cada estratégia pode evoluir independentemente
- Compatibilidade mantida com código existente

#### Testar o Padrão

```bash
python examples_strategy.py
```

## 📝 Notas

- O banco SQLite é criado automaticamente na primeira execução
- Todas as operações incluem tratamento de erros
- Validação de dados para campos obrigatórios
- Timestamps automáticos para criação e atualização
- Documentação completa via Swagger
