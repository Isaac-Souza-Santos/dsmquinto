from functools import wraps
from flask import request, jsonify
from src.models.usuario import Usuario

def require_auth(f):
    """Decorator para proteger rotas que precisam de autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar se há token de autorização
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            from flask import abort
            abort(401, 'Token de autorização necessário')
        
        # Extrair token
        token = token.replace('Bearer ', '')
        
        # Verificar token
        usuario = Usuario.verificar_jwt_token(token)
        if not usuario:
            from flask import abort
            abort(401, 'Token inválido ou expirado')
        
        # Adicionar usuário ao contexto da requisição
        request.current_user = usuario
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_2fa(f):
    """Decorator para rotas que precisam de verificação 2FA"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import abort
        
        # Primeiro verificar autenticação básica
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            abort(401, 'Token de autorização necessário')
        
        token = token.replace('Bearer ', '')
        usuario = Usuario.verificar_jwt_token(token)
        if not usuario:
            abort(401, 'Token inválido ou expirado')
        
        # Verificar se 2FA está configurado
        if not usuario.secret_2fa:
            abort(403, '2FA não configurado')
        
        # Verificar código 2FA no header
        codigo_2fa = request.headers.get('X-2FA-Code')
        if not codigo_2fa:
            abort(401, 'Código 2FA necessário')
        
        # Verificar código 2FA
        if not usuario.verificar_codigo_2fa(codigo_2fa):
            abort(401, 'Código 2FA inválido')
        
        # Adicionar usuário ao contexto
        request.current_user = usuario
        
        return f(*args, **kwargs)
    
    return decorated_function

def get_current_user():
    """Retorna o usuário atual da requisição"""
    return getattr(request, 'current_user', None)
