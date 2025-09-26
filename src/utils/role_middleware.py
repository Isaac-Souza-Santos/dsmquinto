"""
Middleware de Autorização por Níveis de Acesso
"""

from functools import wraps
from flask import request, abort
from src.utils.permissions import verificar_permissao, verificar_nivel_minimo, obter_permissoes_usuario

def require_permission(permission):
    """
    Decorator para verificar permissão específica
    
    Args:
        permission (str): Permissão necessária (ex: 'tarefas:create')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Obter usuário atual
            usuario_atual = getattr(request, 'current_user', None)
            if not usuario_atual:
                abort(401, 'Usuário não autenticado')
            
            # Verificar permissão
            if not verificar_permissao(usuario_atual.nivel_acesso, permission):
                abort(403, f'Permissão insuficiente. Necessário: {permission}')
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_role(minimum_role):
    """
    Decorator para verificar nível mínimo de acesso
    
    Args:
        minimum_role (str): Nível mínimo necessário (ex: 'gerencial')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Obter usuário atual
            usuario_atual = getattr(request, 'current_user', None)
            if not usuario_atual:
                abort(401, 'Usuário não autenticado')
            
            # Verificar nível mínimo
            if not verificar_nivel_minimo(usuario_atual.nivel_acesso, minimum_role):
                abort(403, f'Nível de acesso insuficiente. Necessário: {minimum_role}')
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_admin(f):
    """
    Decorator para rotas que precisam de acesso administrativo
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obter usuário atual
        usuario_atual = getattr(request, 'current_user', None)
        if not usuario_atual:
            abort(401, 'Usuário não autenticado')
        
        # Verificar se é administrador
        if not verificar_nivel_minimo(usuario_atual.nivel_acesso, 'administrativo'):
            abort(403, 'Acesso administrativo necessário')
        
        return f(*args, **kwargs)
    return decorated_function

def require_manager_or_admin(f):
    """
    Decorator para rotas que precisam de acesso gerencial ou administrativo
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obter usuário atual
        usuario_atual = getattr(request, 'current_user', None)
        if not usuario_atual:
            abort(401, 'Usuário não autenticado')
        
        # Verificar se é gerencial ou administrativo
        if not (verificar_nivel_minimo(usuario_atual.nivel_acesso, 'gerencial')):
            abort(403, 'Acesso gerencial ou administrativo necessário')
        
        return f(*args, **kwargs)
    return decorated_function

def get_user_permissions():
    """
    Retorna as permissões do usuário atual
    
    Returns:
        list: Lista de permissões do usuário
    """
    usuario_atual = getattr(request, 'current_user', None)
    if not usuario_atual:
        return []
    
    return obter_permissoes_usuario(usuario_atual.nivel_acesso)

def check_permission(permission):
    """
    Verifica se o usuário atual tem uma permissão específica
    
    Args:
        permission (str): Permissão a verificar
    
    Returns:
        bool: True se tem permissão, False caso contrário
    """
    usuario_atual = getattr(request, 'current_user', None)
    if not usuario_atual:
        return False
    
    return verificar_permissao(usuario_atual.nivel_acesso, permission)
