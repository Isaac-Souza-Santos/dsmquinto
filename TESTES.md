# Testes - Status e Execução

## Status dos Testes

### ✅ Testes Implementados

1. **test_authorization_strategy.py** - Testes do padrão Strategy

   - Testes para VisualizacaoStrategy
   - Testes para GerencialStrategy
   - Testes para AdministrativoStrategy
   - Testes para AuthorizationContext

2. **test_usuario.py** - Testes do modelo Usuario
   - Criação de usuário
   - Validação de email duplicado
   - Verificação de senha
   - Busca por email
   - Geração e verificação de JWT token

## Como Executar os Testes

### Instalação

```bash
pip install -r requirements.txt
```

### Executar Todos os Testes

```bash
pytest tests/ -v
```

### Executar Teste Específico

```bash
pytest tests/test_authorization_strategy.py -v
pytest tests/test_usuario.py -v
```

### Executar com Cobertura

```bash
pytest tests/ --cov=src --cov-report=html
```

## Estrutura dos Testes

```
tests/
├── __init__.py
├── test_authorization_strategy.py
└── test_usuario.py
```

## Notas Importantes

- Os testes de usuário usam banco de dados temporário
- Cada teste cria e limpa seu próprio banco
- Não interfere no banco de dados de produção
- Pytest está configurado no requirements.txt

## Testes Implementados

### Strategy Pattern (9 testes)

- Permissões de visualização
- Permissões gerenciais
- Permissões administrativas
- Validação de níveis inválidos

### Modelo Usuario (6 testes)

- CRUD básico
- Autenticação
- JWT tokens

**Total: 15 testes unitários**
