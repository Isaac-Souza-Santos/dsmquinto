# Tipos de Usuários do Sistema

O sistema possui **3 níveis de acesso** diferentes, organizados em hierarquia:

---

## 👤 1. VISUALIZAÇÃO (`visualizacao`)

**Nível:** 1 (Básico)  
**Descrição:** Apenas visualizar dados

### ✅ Permissões:

- ✅ `tarefas:read` - Ler tarefa específica
- ✅ `tarefas:list` - Listar todas as tarefas

### ❌ Não Pode:

- ❌ Criar tarefas
- ❌ Editar tarefas
- ❌ Deletar tarefas
- ❌ Gerenciar usuários
- ❌ Acessar configurações administrativas

### 📝 Observações:

- Nível padrão para novos usuários registrados
- Ideal para usuários que só precisam consultar informações

---

## 👔 2. GERENCIAL (`gerencial`)

**Nível:** 2 (Intermediário)  
**Descrição:** Gerenciar tarefas e visualizar usuários

### ✅ Permissões:

- ✅ `tarefas:read` - Ler tarefa específica
- ✅ `tarefas:list` - Listar todas as tarefas
- ✅ `tarefas:create` - Criar novas tarefas
- ✅ `tarefas:update` - Atualizar tarefas existentes
- ✅ `tarefas:delete` - Deletar tarefas
- ✅ `usuarios:read` - Visualizar usuário específico
- ✅ `usuarios:list` - Listar todos os usuários

### ❌ Não Pode:

- ❌ Criar usuários
- ❌ Editar usuários
- ❌ Deletar usuários
- ❌ Alterar níveis de acesso
- ❌ Acessar configurações administrativas

### 📝 Observações:

- Pode gerenciar completamente as tarefas
- Pode visualizar informações de usuários, mas não modificá-las
- Ideal para gerentes de projeto e líderes de equipe

---

## 🔐 3. ADMINISTRATIVO (`administrativo`)

**Nível:** 3 (Máximo)  
**Descrição:** Acesso total ao sistema

### ✅ Permissões Completas:

- ✅ `tarefas:read` - Ler tarefa específica
- ✅ `tarefas:list` - Listar todas as tarefas
- ✅ `tarefas:create` - Criar novas tarefas
- ✅ `tarefas:update` - Atualizar tarefas existentes
- ✅ `tarefas:delete` - Deletar tarefas
- ✅ `usuarios:read` - Visualizar usuário específico
- ✅ `usuarios:list` - Listar todos os usuários
- ✅ `usuarios:create` - Criar novos usuários
- ✅ `usuarios:update` - Atualizar usuários existentes
- ✅ `usuarios:delete` - Deletar usuários (soft delete)
- ✅ `usuarios:change_role` - Alterar nível de acesso de usuários
- ✅ `system:admin` - Acesso administrativo ao sistema

### 📝 Observações:

- Controle total sobre o sistema
- Único nível que pode criar e gerenciar usuários
- Único nível que pode alterar níveis de acesso
- Ideal para administradores do sistema

---

## 📊 Comparação de Permissões

| Ação             | Visualização | Gerencial | Administrativo |
| ---------------- | ------------ | --------- | -------------- |
| Ver tarefas      | ✅           | ✅        | ✅             |
| Listar tarefas   | ✅           | ✅        | ✅             |
| Criar tarefas    | ❌           | ✅        | ✅             |
| Editar tarefas   | ❌           | ✅        | ✅             |
| Deletar tarefas  | ❌           | ✅        | ✅             |
| Ver usuários     | ❌           | ✅        | ✅             |
| Listar usuários  | ❌           | ✅        | ✅             |
| Criar usuários   | ❌           | ❌        | ✅             |
| Editar usuários  | ❌           | ❌        | ✅             |
| Deletar usuários | ❌           | ❌        | ✅             |
| Alterar níveis   | ❌           | ❌        | ✅             |

---

## 🔧 Como Funciona

### Criação de Usuários

- **Novos usuários** sempre começam com nível `visualizacao`
- Apenas **administradores** podem alterar o nível de acesso
- Usuários podem ser criados via:
  - Registro público (POST `/auth/register`) - sempre como visualizacao
  - Administrador (POST `/usuarios`) - pode definir nível inicial

### Alteração de Nível

- Apenas usuários **administrativos** podem alterar níveis
- Endpoint: PUT `/usuarios/{id}/change-role`
- Requer permissão `@require_admin`

### Verificação de Permissões

O sistema usa o **padrão Strategy** para verificar permissões:

- Cada nível possui sua própria estratégia
- Verificação automática em cada rota protegida
- Decoradores: `@require_auth`, `@require_permission()`, `@require_admin`

---

## 📝 Exemplos de Uso

### Usuário Visualização

```python
# Pode fazer:
GET /tarefas        # ✅ Listar tarefas
GET /tarefas/1      # ✅ Ver tarefa específica

# Não pode fazer:
POST /tarefas       # ❌ Criar tarefa (403 Forbidden)
PUT /tarefas/1      # ❌ Editar tarefa (403 Forbidden)
DELETE /tarefas/1   # ❌ Deletar tarefa (403 Forbidden)
```

### Usuário Gerencial

```python
# Pode fazer tudo de visualização +:
POST /tarefas       # ✅ Criar tarefa
PUT /tarefas/1      # ✅ Editar tarefa
DELETE /tarefas/1   # ✅ Deletar tarefa
GET /usuarios       # ✅ Listar usuários

# Não pode fazer:
POST /usuarios      # ❌ Criar usuário (403 Forbidden)
PUT /usuarios/1     # ❌ Editar usuário (403 Forbidden)
```

### Usuário Administrativo

```python
# Pode fazer TUDO:
POST /usuarios      # ✅ Criar usuário
PUT /usuarios/1     # ✅ Editar usuário
DELETE /usuarios/1  # ✅ Deletar usuário
PUT /usuarios/1/change-role  # ✅ Alterar nível de acesso
```

---

## 🔐 Segurança

- Cada rota está protegida com decoradores de autenticação
- Permissões verificadas em tempo de execução
- Tokens JWT validados em cada requisição
- Níveis de acesso armazenados no banco de dados
- Soft delete para usuários (marca como inativo, não remove)

---

## 📚 Arquivos Relacionados

- `src/utils/authorization_strategy.py` - Implementação do padrão Strategy
- `src/utils/permissions.py` - Definição de níveis e permissões
- `src/utils/role_middleware.py` - Middleware de verificação
- `src/routes/usuarios.py` - Rotas de gerenciamento de usuários

---

## 🎯 Resumo

| Tipo               | Nível | Pode Gerenciar Tarefas | Pode Gerenciar Usuários | Criar Usuários |
| ------------------ | ----- | ---------------------- | ----------------------- | -------------- |
| **Visualização**   | 1     | ❌ Apenas ver          | ❌                      | ❌             |
| **Gerencial**      | 2     | ✅ Total               | ❌ Apenas ver           | ❌             |
| **Administrativo** | 3     | ✅ Total               | ✅ Total                | ✅             |
