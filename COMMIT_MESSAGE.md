# Mensagem de Commit Sugerida

```
feat: implementar CRUD completo de tarefas com API REST

- Adicionar modelo de tarefa com campos: título, descrição, status
- Implementar rotas REST completas (GET, POST, PUT, DELETE)
- Configurar banco SQLite com persistência automática
- Adicionar documentação Swagger completa
- Incluir tratamento de erros e validação de dados
- Criar exemplos de uso da API
- Configurar .gitignore e .gitattributes apropriados

Rotas implementadas:
- GET /tarefas - Listar todas as tarefas
- POST /tarefas - Criar nova tarefa
- GET /tarefas/{id} - Obter tarefa específica
- PUT /tarefas/{id} - Atualizar tarefa
- DELETE /tarefas/{id} - Remover tarefa

Tecnologias: Flask, Flask-RESTX, SQLite, Python
```

## Comandos Git para subir o projeto:

```bash
# Inicializar repositório (se ainda não existir)
git init

# Adicionar todos os arquivos
git add .

# Fazer o commit inicial
git commit -m "feat: implementar CRUD completo de tarefas com API REST

- Adicionar modelo de tarefa com campos: título, descrição, status
- Implementar rotas REST completas (GET, POST, PUT, DELETE)
- Configurar banco SQLite com persistência automática
- Adicionar documentação Swagger completa
- Incluir tratamento de erros e validação de dados
- Criar exemplos de uso da API
- Configurar .gitignore e .gitattributes apropriados"

# Adicionar repositório remoto (substitua pela sua URL)
git remote add origin <URL_DO_SEU_REPOSITORIO>

# Enviar para o repositório remoto
git push -u origin main
```

## Estrutura final do projeto:

```
dpm/
├── .gitignore              # Arquivos ignorados pelo Git
├── .gitattributes          # Configurações de atributos Git
├── requirements.txt        # Dependências Python
├── README.md              # Documentação completa
├── main.py                # Ponto de entrada da aplicação
├── config.py              # Configurações da API
├── examples.py            # Exemplos de uso da API
├── COMMIT_MESSAGE.md      # Este arquivo
├── tarefas.db             # Banco SQLite (ignorado pelo Git)
└── src/
    ├── __init__.py
    ├── api/
    │   └── app.py         # Configuração Flask
    ├── models/
    │   ├── __init__.py
    │   └── tarefa.py      # Modelo e banco de dados
    ├── routes/
    │   ├── __init__.py
    │   └── api.py         # Rotas da API
    └── utils/
        └── __init__.py
```

