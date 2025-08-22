import os

class Config:
    """Configurações da API de Tarefas"""
    
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Configurações do servidor
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Configurações da API
    API_TITLE = "API de Tarefas"
    API_VERSION = "1.0"
    API_DESCRIPTION = "API CRUD para gerenciamento de tarefas com operações REST completas"
    
    # Configurações do Swagger
    SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTX_VALIDATE = True
    RESTX_MASK_SWAGGER = False
    
    # Configurações do banco de dados
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'tarefas.db')

