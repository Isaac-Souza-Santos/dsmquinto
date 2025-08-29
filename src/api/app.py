from flask import Flask
from flask_restx import Api
from flask_cors import CORS

def create_app():
    """Factory para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurar CORS para permitir conexão do frontend
    # Configuração mais permissiva para desenvolvimento
    CORS(app, 
         origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://localhost:3000"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "Accept"],
         supports_credentials=True,
         max_age=3600
    )
    
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
