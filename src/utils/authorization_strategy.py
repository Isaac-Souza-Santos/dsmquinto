"""
Padrão Strategy para Autorização
Define diferentes estratégias de autorização para cada nível de acesso
"""

from abc import ABC, abstractmethod
from typing import List


class AuthorizationStrategy(ABC):
    """Interface abstrata para estratégias de autorização"""
    
    @abstractmethod
    def can_perform_action(self, action: str) -> bool:
        """
        Verifica se a ação pode ser realizada
        
        Args:
            action (str): Ação a verificar (ex: 'tarefas:create')
        
        Returns:
            bool: True se pode realizar a ação
        """
        pass
    
    @abstractmethod
    def get_allowed_actions(self) -> List[str]:
        """
        Retorna todas as ações permitidas
        
        Returns:
            List[str]: Lista de ações permitidas
        """
        pass
    
    @abstractmethod
    def get_level_name(self) -> str:
        """
        Retorna o nome do nível de acesso
        
        Returns:
            str: Nome do nível
        """
        pass


class VisualizacaoStrategy(AuthorizationStrategy):
    """Estratégia para nível de visualização - apenas leitura"""
    
    ALLOWED_ACTIONS = [
        'tarefas:read',
        'tarefas:list'
    ]
    
    def can_perform_action(self, action: str) -> bool:
        return action in self.ALLOWED_ACTIONS
    
    def get_allowed_actions(self) -> List[str]:
        return self.ALLOWED_ACTIONS.copy()
    
    def get_level_name(self) -> str:
        return 'visualizacao'


class GerencialStrategy(AuthorizationStrategy):
    """Estratégia para nível gerencial - gerenciar tarefas e usuários"""
    
    ALLOWED_ACTIONS = [
        'tarefas:read',
        'tarefas:list',
        'tarefas:create',
        'tarefas:update',
        'tarefas:delete',
        'usuarios:read',
        'usuarios:list'
    ]
    
    def can_perform_action(self, action: str) -> bool:
        return action in self.ALLOWED_ACTIONS
    
    def get_allowed_actions(self) -> List[str]:
        return self.ALLOWED_ACTIONS.copy()
    
    def get_level_name(self) -> str:
        return 'gerencial'


class AdministrativoStrategy(AuthorizationStrategy):
    """Estratégia para nível administrativo - acesso total"""
    
    ALLOWED_ACTIONS = [
        'tarefas:read',
        'tarefas:list',
        'tarefas:create',
        'tarefas:update',
        'tarefas:delete',
        'usuarios:read',
        'usuarios:list',
        'usuarios:create',
        'usuarios:update',
        'usuarios:delete',
        'usuarios:change_role',
        'system:admin'
    ]
    
    def can_perform_action(self, action: str) -> bool:
        return action in self.ALLOWED_ACTIONS
    
    def get_allowed_actions(self) -> List[str]:
        return self.ALLOWED_ACTIONS.copy()
    
    def get_level_name(self) -> str:
        return 'administrativo'


class AuthorizationContext:
    """Contexto que utiliza a estratégia de autorização"""
    
    def __init__(self, nivel_acesso: str):
        """
        Inicializa o contexto com a estratégia apropriada
        
        Args:
            nivel_acesso (str): Nível de acesso do usuário
        """
        self.strategy = self._create_strategy(nivel_acesso)
    
    def _create_strategy(self, nivel_acesso: str) -> AuthorizationStrategy:
        """
        Factory method para criar a estratégia apropriada
        
        Args:
            nivel_acesso (str): Nível de acesso
        
        Returns:
            AuthorizationStrategy: Estratégia apropriada
        """
        strategies = {
            'visualizacao': VisualizacaoStrategy(),
            'gerencial': GerencialStrategy(),
            'administrativo': AdministrativoStrategy()
        }
        
        strategy = strategies.get(nivel_acesso)
        if not strategy:
            raise ValueError(f"Nível de acesso inválido: {nivel_acesso}")
        
        return strategy
    
    def can_perform_action(self, action: str) -> bool:
        """
        Verifica se a ação pode ser realizada usando a estratégia atual
        
        Args:
            action (str): Ação a verificar
        
        Returns:
            bool: True se pode realizar a ação
        """
        return self.strategy.can_perform_action(action)
    
    def get_allowed_actions(self) -> List[str]:
        """
        Retorna todas as ações permitidas
        
        Returns:
            List[str]: Lista de ações permitidas
        """
        return self.strategy.get_allowed_actions()
    
    def get_level_name(self) -> str:
        """
        Retorna o nome do nível de acesso
        
        Returns:
            str: Nome do nível
        """
        return self.strategy.get_level_name()


def create_authorization_context(nivel_acesso: str) -> AuthorizationContext:
    """
    Função helper para criar contexto de autorização
    
    Args:
        nivel_acesso (str): Nível de acesso do usuário
    
    Returns:
        AuthorizationContext: Contexto de autorização
    """
    return AuthorizationContext(nivel_acesso)

