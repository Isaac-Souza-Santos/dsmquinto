"""
Testes unitários para o padrão Strategy de autorização
"""
import pytest
from src.utils.authorization_strategy import (
    create_authorization_context,
    VisualizacaoStrategy,
    GerencialStrategy,
    AdministrativoStrategy
)


class TestVisualizacaoStrategy:
    """Testes para estratégia de visualização"""

    def test_can_read_tasks(self):
        """Deve permitir ler tarefas"""
        strategy = VisualizacaoStrategy()
        assert strategy.can_perform_action('tarefas:read') is True

    def test_can_list_tasks(self):
        """Deve permitir listar tarefas"""
        strategy = VisualizacaoStrategy()
        assert strategy.can_perform_action('tarefas:list') is True

    def test_cannot_create_tasks(self):
        """Não deve permitir criar tarefas"""
        strategy = VisualizacaoStrategy()
        assert strategy.can_perform_action('tarefas:create') is False

    def test_get_allowed_actions(self):
        """Deve retornar apenas ações permitidas"""
        strategy = VisualizacaoStrategy()
        actions = strategy.get_allowed_actions()
        assert 'tarefas:read' in actions
        assert 'tarefas:list' in actions
        assert len(actions) == 2


class TestGerencialStrategy:
    """Testes para estratégia gerencial"""

    def test_can_manage_tasks(self):
        """Deve permitir gerenciar tarefas"""
        strategy = GerencialStrategy()
        assert strategy.can_perform_action('tarefas:create') is True
        assert strategy.can_perform_action('tarefas:update') is True
        assert strategy.can_perform_action('tarefas:delete') is True

    def test_can_view_users(self):
        """Deve permitir visualizar usuários"""
        strategy = GerencialStrategy()
        assert strategy.can_perform_action('usuarios:read') is True
        assert strategy.can_perform_action('usuarios:list') is True

    def test_cannot_admin_users(self):
        """Não deve permitir administrar usuários"""
        strategy = GerencialStrategy()
        assert strategy.can_perform_action('usuarios:create') is False
        assert strategy.can_perform_action('system:admin') is False


class TestAdministrativoStrategy:
    """Testes para estratégia administrativa"""

    def test_can_do_everything(self):
        """Deve permitir todas as ações"""
        strategy = AdministrativoStrategy()
        assert strategy.can_perform_action('tarefas:create') is True
        assert strategy.can_perform_action('usuarios:create') is True
        assert strategy.can_perform_action('system:admin') is True

    def test_get_allowed_actions(self):
        """Deve retornar todas as ações permitidas"""
        strategy = AdministrativoStrategy()
        actions = strategy.get_allowed_actions()
        assert 'system:admin' in actions
        assert len(actions) > 5


class TestAuthorizationContext:
    """Testes para contexto de autorização"""

    def test_create_visualizacao_context(self):
        """Deve criar contexto de visualização"""
        context = create_authorization_context('visualizacao')
        assert context.get_level_name() == 'visualizacao'
        assert context.can_perform_action('tarefas:read') is True
        assert context.can_perform_action('tarefas:create') is False

    def test_create_gerencial_context(self):
        """Deve criar contexto gerencial"""
        context = create_authorization_context('gerencial')
        assert context.get_level_name() == 'gerencial'
        assert context.can_perform_action('tarefas:create') is True
        assert context.can_perform_action('usuarios:create') is False

    def test_create_administrativo_context(self):
        """Deve criar contexto administrativo"""
        context = create_authorization_context('administrativo')
        assert context.get_level_name() == 'administrativo'
        assert context.can_perform_action('system:admin') is True

    def test_invalid_level(self):
        """Deve lançar erro para nível inválido"""
        with pytest.raises(ValueError):
            create_authorization_context('invalido')

