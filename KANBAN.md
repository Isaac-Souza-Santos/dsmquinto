# Documentação do Processo de Desenvolvimento - Metodologia Kanban

## O que é Kanban

Kanban é uma metodologia ágil de gerenciamento de projetos que utiliza um sistema visual de cartões e colunas para representar o fluxo de trabalho.

## Fluxo de Trabalho

```
Backlog → Em Desenvolvimento → Testes → Concluído
```

### Status das Tarefas

- **Pendente**: Tarefa identificada, ainda não iniciada
- **Em Progresso**: Tarefa sendo desenvolvida
- **Concluída**: Tarefa finalizada e testada

---

## 📋 REQUISITOS CONCLUÍDOS

### 1. ✅ Implementação de API REST

#### Backend - Estrutura Base

- [x] Configuração do Flask e Flask-RESTX
- [x] Estrutura de pastas organizada (`src/api/`, `src/routes/`, `src/models/`)
- [x] Criação do arquivo `main.py` como ponto de entrada
- [x] Configuração do CORS para permitir requisições do frontend
- [x] Documentação Swagger configurada em `/docs`

#### API e Documentação

- [x] Integração com Flask-RESTX para documentação automática
- [x] Modelos de API definidos para validação
- [x] Namespaces organizados por funcionalidade
- [x] Endpoints documentados com exemplos

---

### 2. ✅ Endpoints Básicos - CRUD de Tarefas

#### Rotas de Tarefas

- [x] GET `/tarefas` - Listar todas as tarefas
- [x] POST `/tarefas` - Criar nova tarefa
- [x] GET `/tarefas/{id}` - Obter tarefa específica
- [x] PUT `/tarefas/{id}` - Atualizar tarefa existente
- [x] DELETE `/tarefas/{id}` - Deletar tarefa

#### Validação e Tratamento

- [x] Validação de campos obrigatórios
- [x] Tratamento de erros (400, 404, 500)
- [x] Mensagens de erro descritivas
- [x] Validação de status (pendente/concluida)

---

### 3. ✅ Responsividade da Interface

#### Layout Responsivo

- [x] Media queries implementadas no CSS
- [x] Breakpoint para tablet (768px)
- [x] Breakpoint para mobile (480px)
- [x] Grid responsivo para cards do dashboard
- [x] Layout adaptativo para lista de tarefas

#### Interface Frontend

- [x] HTML semântico estruturado
- [x] CSS moderno com variáveis
- [x] Layout de duas colunas (dashboard/tarefas | formulário)
- [x] Cards do dashboard quadrados e lado a lado
- [x] Formulários responsivos

---

### 4. ✅ Autenticação de Usuário

#### Sistema de Login

- [x] POST `/auth/register` - Registro de usuário
- [x] POST `/auth/login` - Login com email e senha
- [x] GET `/auth/me` - Obter usuário atual
- [x] POST `/auth/logout` - Logout (invalida token)

#### Segurança

- [x] Hash de senhas com Werkzeug
- [x] JWT tokens para autenticação
- [x] Tokens com expiração (7 dias)
- [x] Sessões armazenadas no banco de dados
- [x] Verificação de token em cada requisição

#### Autenticação 2FA

- [x] Geração de secret para Google Authenticator
- [x] Geração de QR Code para configuração
- [x] Verificação de código 2FA
- [x] Rotas para setup e verificação de 2FA

#### Frontend de Autenticação

- [x] Página de login (`login.html`)
- [x] Página de registro
- [x] Verificação de token no localStorage
- [x] Redirecionamento automático se não autenticado
- [x] Função auxiliar `getAuthHeaders()` para incluir token

---

### 5. ✅ Banco de Dados

#### Estrutura SQLite

- [x] Criação automática do banco `tarefas.db`
- [x] Tabela `tarefas` com campos completos
- [x] Tabela `usuarios` para autenticação
- [x] Tabela `sessoes` para tokens JWT

#### Modelos

- [x] Modelo de Tarefa (`src/models/tarefa.py`)
- [x] Modelo de Usuário (`src/models/usuario.py`)
- [x] Inicialização automática das tabelas
- [x] Funções auxiliares de conexão

#### Funcionalidades

- [x] Timestamps automáticos (data_criacao, data_atualizacao)
- [x] Soft delete para usuários
- [x] Relacionamento entre tarefas e usuários

---

### 6. ✅ CRUD de Usuários

#### Rotas de Usuários

- [x] POST `/usuarios` - Criar usuário
- [x] GET `/usuarios` - Listar todos os usuários
- [x] GET `/usuarios/{id}` - Obter usuário específico
- [x] PUT `/usuarios/{id}` - Atualizar usuário
- [x] DELETE `/usuarios/{id}` - Deletar usuário (soft delete)

#### Funcionalidades

- [x] Validação de email único
- [x] Criação com nível de acesso padrão
- [x] Atualização de nível de acesso
- [x] Soft delete (ativo/inativo)

---

### 7. ✅ Permissões de Acesso

#### Níveis de Acesso

- [x] Nível `visualizacao` - Apenas leitura
- [x] Nível `gerencial` - Gerenciar tarefas e usuários
- [x] Nível `administrativo` - Acesso total

#### Sistema de Permissões

- [x] Decorador `@require_auth` para autenticação
- [x] Decorador `@require_permission()` para permissões específicas
- [x] Decorador `@require_admin` para acesso administrativo
- [x] Decorador `@require_manager_or_admin` para gerencial+

#### Middleware

- [x] `auth_middleware.py` - Verificação de token JWT
- [x] `role_middleware.py` - Verificação de permissões
- [x] `permissions.py` - Lógica de verificação de permissões

#### Permissões por Ação

- [x] `tarefas:list` - Listar tarefas
- [x] `tarefas:read` - Ler tarefa específica
- [x] `tarefas:create` - Criar tarefa
- [x] `tarefas:update` - Atualizar tarefa
- [x] `tarefas:delete` - Deletar tarefa
- [x] `usuarios:*` - Gerenciar usuários
- [x] `system:admin` - Acesso administrativo

---

### 8. ✅ Documentação Kanban

#### Documentação do Processo

- [x] Documento `KANBAN.md` criado
- [x] Metodologia Kanban aplicada e documentada
- [x] Fluxo de trabalho documentado
- [x] Tarefas organizadas por status

---

### 9. ✅ TDD - Test-Driven Development

#### Estrutura de Testes

- [x] Diretório `tests/` criado
- [x] Framework pytest adicionado ao `requirements.txt`
- [x] Arquivo `__init__.py` para inicializar testes

#### Testes Implementados

- [x] `test_authorization_strategy.py` - 9 testes do padrão Strategy
  - [x] Testes para VisualizacaoStrategy
  - [x] Testes para GerencialStrategy
  - [x] Testes para AdministrativoStrategy
  - [x] Testes para AuthorizationContext
- [x] `test_usuario.py` - 6 testes do modelo Usuario
  - [x] Teste de criação de usuário
  - [x] Teste de email duplicado
  - [x] Teste de verificação de senha
  - [x] Teste de busca por email
  - [x] Teste de geração de JWT token
  - [x] Teste de verificação de JWT token

#### Configuração

- [x] Banco de dados temporário para testes
- [x] Fixtures para setup/teardown
- [x] Suporte a variável de ambiente `DATABASE_PATH`

---

### 10. ✅ Design Patterns

#### Factory Method Pattern

- [x] `create_app()` em `src/api/app.py`
- [x] `create_routes()` em `src/routes/api.py`
- [x] `create_auth_routes()` em `src/routes/auth.py`
- [x] `create_user_routes()` em `src/routes/usuarios.py`
- [x] `create_models()` para modelos da API

#### Strategy Pattern

- [x] Interface `AuthorizationStrategy` definida
- [x] `VisualizacaoStrategy` implementada
- [x] `GerencialStrategy` implementada
- [x] `AdministrativoStrategy` implementada
- [x] `AuthorizationContext` para seleção de estratégia
- [x] Factory `create_authorization_context()`

#### Decorator Pattern

- [x] `@require_auth` - Middleware de autenticação
- [x] `@require_permission()` - Middleware de permissão
- [x] `@require_admin` - Middleware de admin
- [x] `@require_manager_or_admin` - Middleware de gerencial+
- [x] `@require_2fa` - Middleware de 2FA

---

## 🔧 CORREÇÕES E MELHORIAS IMPLEMENTADAS

### Autenticação

- [x] Correção do formato do token JWT (bytes para string)
- [x] Uso consistente de timezone UTC em todas as datas
- [x] Verificação de expiração de sessão corrigida
- [x] Função `getAuthHeaders()` no frontend para garantir token

### Frontend

- [x] Layout de duas colunas (dashboard/tarefas | formulário)
- [x] Cards do dashboard menores e quadrados
- [x] Lista de tarefas abaixo dos cards
- [x] Formulário na segunda coluna
- [x] Teste de conexão com API corrigido

### Testes

- [x] Correção do teste de verificação de senha
- [x] Suporte a banco temporário nos testes
- [x] Correção de avisos de deprecação (datetime.utcnow)

---

## 📊 Resumo Final

### Estatísticas

- **Total de Requisitos:** 10
- **Concluídos:** 10 (100%)
- **Em Desenvolvimento:** 0
- **Pendentes:** 0

### Arquivos Criados/Modificados

- **Backend:** 15+ arquivos
- **Frontend:** 3 arquivos principais (HTML, CSS, JS)
- **Testes:** 3 arquivos
- **Documentação:** 5 arquivos MD

### Funcionalidades

- **Endpoints API:** 15+
- **Níveis de Acesso:** 3
- **Design Patterns:** 3
- **Testes Unitários:** 15

---

## 🎯 Benefícios da Metodologia Kanban

- ✅ Visualização clara do progresso
- ✅ Organização eficiente das tarefas
- ✅ Priorização facilitada
- ✅ Rastreamento de status detalhado
- ✅ Comunicação melhorada sobre o que foi feito
- ✅ Documentação completa do desenvolvimento

---

## 🛠️ Ferramentas Utilizadas

- **Controle de Versão:** Git
- **Gerenciamento de Tarefas:** Metodologia Kanban
- **Documentação:** Markdown
- **Backend:** Python 3, Flask, Flask-RESTX, SQLite
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Testes:** Pytest
- **Autenticação:** JWT, PyOTP (2FA)

---

## 📝 Conclusão

A metodologia Kanban foi fundamental para organizar o desenvolvimento desta aplicação, permitindo:

1. **Visibilidade:** Cada tarefa foi rastreada desde o backlog até a conclusão
2. **Organização:** Tarefas grandes foram divididas em mini tarefas gerenciáveis
3. **Foco:** Priorização clara do que deveria ser feito primeiro
4. **Documentação:** Registro completo de tudo que foi implementado

---
