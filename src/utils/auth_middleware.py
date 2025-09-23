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
            return jsonify({
                'error': 'Token de autorização necessário',
                'message': 'Adicione o header Authorization: Bearer <token>'
            }), 401
        
        # Extrair token
        token = token.replace('Bearer ', '')
        
        # Verificar token
        usuario = Usuario.verificar_jwt_token(token)
        if not usuario:
            return jsonify({
                'error': 'Token inválido ou expirado',
                'message': 'Faça login novamente'
            }), 401
        
        # Adicionar usuário ao contexto da requisição
        request.current_user = usuario
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_2fa(f):
    """Decorator para rotas que precisam de verificação 2FA"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Primeiro verificar autenticação básica
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({
                'error': 'Token de autorização necessário',
                'message': 'Adicione o header Authorization: Bearer <token>'
            }), 401
        
        token = token.replace('Bearer ', '')
        usuario = Usuario.verificar_jwt_token(token)
        if not usuario:
            return jsonify({
                'error': 'Token inválido ou expirado',
                'message': 'Faça login novamente'
            }), 401
        
        # Verificar se 2FA está configurado
        if not usuario.secret_2fa:
            return jsonify({
                'error': '2FA não configurado',
                'message': 'Configure o 2FA primeiro em /auth/setup-2fa'
            }), 403
        
        # Verificar código 2FA no header
        codigo_2fa = request.headers.get('X-2FA-Code')
        if not codigo_2fa:
            return jsonify({
                'error': 'Código 2FA necessário',
                'message': 'Adicione o header X-2FA-Code com o código do Google Authenticator'
            }), 401
        
        # Verificar código 2FA
        if not usuario.verificar_codigo_2fa(codigo_2fa):
            return jsonify({
                'error': 'Código 2FA inválido',
                'message': 'Verifique o código do Google Authenticator'
            }), 401
        
        # Adicionar usuário ao contexto
        request.current_user = usuario
        
        return f(*args, **kwargs)
    
    return decorated_function

def get_current_user():
    """Retorna o usuário atual da requisição"""
    return getattr(request, 'current_user', None)
