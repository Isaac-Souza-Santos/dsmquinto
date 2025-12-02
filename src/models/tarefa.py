from flask_restx import fields
import sqlite3
import os
from datetime import datetime

def create_models(api):
    """Cria os modelos para Swagger"""
    
    # Modelo para tarefa
    tarefa_model = api.model('Tarefa', {
        'titulo': fields.String(required=True, description='Título da tarefa'),
        'descricao': fields.String(description='Descrição da tarefa'),
        'status': fields.String(enum=['pendente', 'em_progresso', 'concluida'], description='Status da tarefa', default='pendente')
    })
    
    # Modelo para resposta de tarefa
    tarefa_resposta_model = api.model('TarefaResposta', {
        'id': fields.Integer(description='ID da tarefa'),
        'titulo': fields.String(description='Título da tarefa'),
        'descricao': fields.String(description='Descrição da tarefa'),
        'status': fields.String(description='Status da tarefa'),
        'data_criacao': fields.String(description='Data de criação'),
        'data_atualizacao': fields.String(description='Data de atualização')
    })
    
    # Modelo para lista de tarefas
    tarefa_lista_model = api.model('TarefaLista', {
        'tarefas': fields.List(fields.Nested(tarefa_resposta_model), description='Lista de tarefas'),
        'total': fields.Integer(description='Total de tarefas')
    })
    
    # Modelo para mensagem de resposta
    mensagem_model = api.model('Mensagem', {
        'message': fields.String(description='Mensagem de resposta'),
        'status': fields.String(description='Status da operação')
    })
    
    return tarefa_model, tarefa_resposta_model, tarefa_lista_model, mensagem_model

def init_database():
    """Inicializa o banco de dados SQLite"""
    db_path = 'tarefas.db'
    
    # Criar tabela se não existir
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT DEFAULT 'pendente',
            data_criacao TEXT NOT NULL,
            data_atualizacao TEXT NOT NULL,
            usuario_id INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Retorna uma conexão com o banco de dados"""
    return sqlite3.connect('tarefas.db')
