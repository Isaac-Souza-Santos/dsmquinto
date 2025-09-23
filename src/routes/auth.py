from flask import request
from flask_restx import Resource, Namespace
from datetime import datetime

def create_auth_routes(api):
    """Cria as rotas de autenticação"""
    
    # Namespace para autenticação
    auth_ns = Namespace('auth', description='Autenticação e gerenciamento de usuários')
    
    # Criar modelos
    from src.models.usuario import create_auth_models, init_auth_database, Usuario
    usuario_registro_model, usuario_login_model, verificar_2fa_model, usuario_resposta_model, login_resposta_model = create_auth_models(api)
    
    # Inicializar banco de dados de autenticação
    init_auth_database()
    
    @auth_ns.route('/register')
    class UsuarioRegistro(Resource):
        @auth_ns.doc('registrar_usuario')
        @auth_ns.expect(usuario_registro_model)
        @auth_ns.response(201, 'Usuário criado com sucesso', usuario_resposta_model)
        @auth_ns.response(400, 'Erro de validação')
        def post(self):
            """Registrar novo usuário"""
            try:
                dados = request.get_json()
                if not dados:
                    auth_ns.abort(400, "Dados são obrigatórios")
                
                # Validar campos obrigatórios
                if not dados.get('nome'):
                    auth_ns.abort(400, "Campo 'nome' é obrigatório")
                if not dados.get('email'):
                    auth_ns.abort(400, "Campo 'email' é obrigatório")
                if not dados.get('senha'):
                    auth_ns.abort(400, "Campo 'senha' é obrigatório")
                
                if len(dados['senha']) < 6:
                    auth_ns.abort(400, "Senha deve ter pelo menos 6 caracteres")
                
                # Criar usuário
                usuario = Usuario.criar(
                    nome=dados['nome'],
                    email=dados['email'],
                    senha=dados['senha']
                )
                
                return usuario.to_dict(), 201
                
            except ValueError as e:
                auth_ns.abort(400, str(e))
            except Exception as e:
                auth_ns.abort(500, f"Erro ao criar usuário: {str(e)}")
    
    @auth_ns.route('/login')
    class UsuarioLogin(Resource):
        @auth_ns.doc('login_usuario')
        @auth_ns.expect(usuario_login_model)
        @auth_ns.response(200, 'Login realizado com sucesso', login_resposta_model)
        @auth_ns.response(401, 'Credenciais inválidas')
        def post(self):
            """Login do usuário"""
            try:
                dados = request.get_json()
                if not dados or not dados.get('email') or not dados.get('senha'):
                    auth_ns.abort(400, "Email e senha são obrigatórios")
                
                # Buscar usuário
                usuario = Usuario.buscar_por_email(dados['email'])
                if not usuario or not usuario.verificar_senha(dados['senha']):
                    auth_ns.abort(401, "Email ou senha inválidos")
                
                # Gerar token JWT
                token = usuario.gerar_jwt_token()
                
                # Gerar QR Code para 2FA (se ainda não configurado)
                qr_code_url = None
                if usuario.secret_2fa:
                    qr_code_url = usuario.gerar_qr_code_2fa()
                
                return {
                    'usuario': usuario.to_dict(),
                    'token': token,
                    '2fa_necessario': False,  # Por enquanto, 2FA é opcional
                    'qr_code_url': qr_code_url
                }
                
            except Exception as e:
                auth_ns.abort(500, f"Erro ao fazer login: {str(e)}")
    
    @auth_ns.route('/verify-2fa')
    class Verificar2FA(Resource):
        @auth_ns.doc('verificar_2fa')
        @auth_ns.expect(verificar_2fa_model)
        @auth_ns.response(200, '2FA verificado com sucesso')
        @auth_ns.response(401, 'Código 2FA inválido')
        def post(self):
            """Verificar código 2FA"""
            try:
                dados = request.get_json()
                if not dados or not dados.get('codigo'):
                    auth_ns.abort(400, "Código é obrigatório")
                
                # Buscar usuário pelo token JWT no header
                token = request.headers.get('Authorization')
                if not token or not token.startswith('Bearer '):
                    auth_ns.abort(401, "Token de autorização necessário")
                
                token = token.replace('Bearer ', '')
                usuario = Usuario.verificar_jwt_token(token)
                if not usuario:
                    auth_ns.abort(401, "Token inválido")
                
                # Verificar código 2FA
                if not usuario.verificar_codigo_2fa(dados['codigo']):
                    auth_ns.abort(401, "Código 2FA inválido")
                
                return {
                    'message': '2FA verificado com sucesso',
                    'status': 'sucesso'
                }
                
            except Exception as e:
                auth_ns.abort(500, f"Erro ao verificar 2FA: {str(e)}")
    
    @auth_ns.route('/me')
    class UsuarioAtual(Resource):
        @auth_ns.doc('obter_usuario_atual')
        @auth_ns.response(200, 'Usuário atual', usuario_resposta_model)
        @auth_ns.response(401, 'Token inválido')
        def get(self):
            """Obter dados do usuário atual"""
            try:
                # Buscar usuário pelo token JWT
                token = request.headers.get('Authorization')
                if not token or not token.startswith('Bearer '):
                    auth_ns.abort(401, "Token de autorização necessário")
                
                token = token.replace('Bearer ', '')
                usuario = Usuario.verificar_jwt_token(token)
                if not usuario:
                    auth_ns.abort(401, "Token inválido")
                
                return usuario.to_dict()
                
            except Exception as e:
                auth_ns.abort(500, f"Erro ao obter usuário: {str(e)}")
    
    @auth_ns.route('/logout')
    class UsuarioLogout(Resource):
        @auth_ns.doc('logout_usuario')
        @auth_ns.response(200, 'Logout realizado com sucesso')
        @auth_ns.response(401, 'Token inválido')
        def post(self):
            """Logout do usuário"""
            try:
                # Buscar usuário pelo token JWT
                token = request.headers.get('Authorization')
                if not token or not token.startswith('Bearer '):
                    auth_ns.abort(401, "Token de autorização necessário")
                
                token = token.replace('Bearer ', '')
                usuario = Usuario.verificar_jwt_token(token)
                if not usuario:
                    auth_ns.abort(401, "Token inválido")
                
                # Desativar token no banco
                from src.models.usuario import get_db_connection
                conn = get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute('UPDATE sessoes SET ativo = 0 WHERE token = ?', (token,))
                conn.commit()
                conn.close()
                
                return {
                    'message': 'Logout realizado com sucesso',
                    'status': 'sucesso'
                }
                
            except Exception as e:
                auth_ns.abort(500, f"Erro ao fazer logout: {str(e)}")
    
    @auth_ns.route('/setup-2fa')
    class Setup2FA(Resource):
        @auth_ns.doc('configurar_2fa')
        @auth_ns.response(200, 'QR Code gerado para configuração 2FA')
        @auth_ns.response(401, 'Token inválido')
        def get(self):
            """Configurar 2FA para o usuário"""
            try:
                # Buscar usuário pelo token JWT
                token = request.headers.get('Authorization')
                if not token or not token.startswith('Bearer '):
                    auth_ns.abort(401, "Token de autorização necessário")
                
                token = token.replace('Bearer ', '')
                usuario = Usuario.verificar_jwt_token(token)
                if not usuario:
                    auth_ns.abort(401, "Token inválido")
                
                # Gerar QR Code
                qr_code_url = usuario.gerar_qr_code_2fa()
                
                return {
                    'qr_code_url': qr_code_url,
                    'secret': usuario.secret_2fa,
                    'message': 'Configure o Google Authenticator com o QR Code'
                }
                
            except Exception as e:
                auth_ns.abort(500, f"Erro ao configurar 2FA: {str(e)}")
    
    return auth_ns
