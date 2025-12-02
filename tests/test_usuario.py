"""
Testes unitários para o modelo de usuário
"""
import pytest
import os
import tempfile
import sqlite3
from src.models.usuario import Usuario, init_auth_database


@pytest.fixture
def temp_db():
    """Cria um banco de dados temporário para testes"""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.environ['DATABASE_PATH'] = db_path
    
    # Inicializar banco
    init_auth_database()
    
    yield db_path
    
    # Limpar
    os.close(db_fd)
    os.unlink(db_path)
    if 'DATABASE_PATH' in os.environ:
        del os.environ['DATABASE_PATH']


class TestUsuario:
    """Testes para a classe Usuario"""

    def test_criar_usuario(self, temp_db):
        """Deve criar um novo usuário"""
        usuario = Usuario.criar(
            nome="Teste User",
            email="teste@teste.com",
            senha="senha123"
        )
        
        assert usuario.id is not None
        assert usuario.nome == "Teste User"
        assert usuario.email == "teste@teste.com"
        assert usuario.nivel_acesso == "visualizacao"
        assert usuario.ativo is True

    def test_email_duplicado(self, temp_db):
        """Não deve permitir email duplicado"""
        Usuario.criar(
            nome="User 1",
            email="duplicado@teste.com",
            senha="senha123"
        )
        
        with pytest.raises(ValueError, match="Email já cadastrado"):
            Usuario.criar(
                nome="User 2",
                email="duplicado@teste.com",
                senha="senha456"
            )

    def test_verificar_senha(self, temp_db):
        """Deve verificar senha corretamente"""
        Usuario.criar(
            nome="Teste",
            email="teste2@teste.com",
            senha="senha123"
        )
        
        # Buscar usuário do banco para ter senha_hash
        usuario = Usuario.buscar_por_email("teste2@teste.com")
        assert usuario is not None
        
        assert usuario.verificar_senha("senha123") is True
        assert usuario.verificar_senha("senha_errada") is False

    def test_buscar_por_email(self, temp_db):
        """Deve buscar usuário por email"""
        Usuario.criar(
            nome="Buscar",
            email="buscar@teste.com",
            senha="senha123"
        )
        
        usuario = Usuario.buscar_por_email("buscar@teste.com")
        assert usuario is not None
        assert usuario.email == "buscar@teste.com"
        
        # Email não existe
        usuario_inexistente = Usuario.buscar_por_email("naoexiste@teste.com")
        assert usuario_inexistente is None

    def test_gerar_jwt_token(self, temp_db):
        """Deve gerar token JWT"""
        usuario = Usuario.criar(
            nome="Token",
            email="token@teste.com",
            senha="senha123"
        )
        
        token = usuario.gerar_jwt_token()
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_verificar_jwt_token(self, temp_db):
        """Deve verificar token JWT válido"""
        usuario = Usuario.criar(
            nome="JWT",
            email="jwt@teste.com",
            senha="senha123"
        )
        
        token = usuario.gerar_jwt_token()
        usuario_verificado = Usuario.verificar_jwt_token(token)
        
        assert usuario_verificado is not None
        assert usuario_verificado.id == usuario.id
        assert usuario_verificado.email == usuario.email

