from flask import Flask
from flask_restx import Api

def create_app():
    """Factory para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configuração da API
    api = Api(app, 
        title="API de Tarefas",
        description="API CRUD para gerenciamento de tarefas com operações REST completas",
        version="1.0",
        doc="/docs"
    )
    
    # Criar e registrar rotas
    from src.routes.api import create_routes
    api_ns = create_routes(api)
    api.add_namespace(api_ns)
    
    return app, api
