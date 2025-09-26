"""
Rotas para gerenciamento de usuários e níveis de acesso
"""

from flask import request
from flask_restx import Resource, Namespace, fields
from datetime import datetime
from src.models.usuario import Usuario, create_auth_models, init_auth_database
from src.utils.role_middleware import require_admin, require_manager_or_admin, require_permission
from src.utils.permissions import obter_niveis_disponiveis, validar_nivel_acesso

def create_user_routes(api):
    """Cria as rotas para gerenciamento de usuários"""
    
    # Namespace para usuários
    user_ns = Namespace('usuarios', description='Gerenciamento de usuários e níveis de acesso')
    
    # Criar modelos
    usuario_registro_model, usuario_login_model, verificar_2fa_model, usuario_resposta_model, login_resposta_model = create_auth_models(api)
    
    # Inicializar banco de dados
    init_auth_database()
    
    # Modelo para atualização de usuário
    usuario_update_model = user_ns.model('UsuarioUpdate', {
        'nome': fields.String(description='Nome do usuário'),
        'nivel_acesso': fields.String(enum=['visualizacao', 'gerencial', 'administrativo'], description='Nível de acesso'),
        'ativo': fields.Boolean(description='Status ativo/inativo')
    })
    
    # Modelo para resposta de níveis de acesso
    niveis_model = user_ns.model('NiveisAcesso', {
        'niveis': fields.Raw(description='Níveis de acesso disponíveis')
    })
    
    @user_ns.route('/')
    class UsuariosList(Resource):
        @user_ns.doc('listar_usuarios')
        @user_ns.response(200, 'Sucesso')
        @require_manager_or_admin
        def get(self):
            """Listar todos os usuários (apenas gerencial e administrativo)"""
            try:
                conn = Usuario.get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM usuarios ORDER BY data_criacao DESC')
                usuarios = cursor.fetchall()
                
                usuarios_list = []
                for usuario in usuarios:
                    usuarios_list.append({
                        'id': usuario[0],
                        'nome': usuario[1],
                        'email': usuario[2],
                        'nivel_acesso': usuario[5],
                        'ativo': bool(usuario[6]),
                        'data_criacao': usuario[7]
                    })
                
                conn.close()
                
                return {
                    'usuarios': usuarios_list,
                    'total': len(usuarios_list)
                }
            except Exception as e:
                user_ns.abort(500, f"Erro ao listar usuários: {str(e)}")
        
        @user_ns.doc('criar_usuario')
        @user_ns.expect(usuario_registro_model)
        @user_ns.response(201, 'Usuário criado com sucesso', usuario_resposta_model)
        @user_ns.response(400, 'Erro de validação')
        @require_admin
        def post(self):
            """Criar novo usuário (apenas administrativo)"""
            try:
                dados = request.get_json()
                if not dados:
                    user_ns.abort(400, "Dados são obrigatórios")
                
                nome = dados.get('nome')
                email = dados.get('email')
                senha = dados.get('senha')
                nivel_acesso = dados.get('nivel_acesso', 'visualizacao')
                
                if not nome or not email or not senha:
                    user_ns.abort(400, "Nome, email e senha são obrigatórios")
                
                if not validar_nivel_acesso(nivel_acesso):
                    user_ns.abort(400, "Nível de acesso inválido")
                
                # Criar usuário
                usuario = Usuario.criar(nome, email, senha)
                
                # Atualizar nível de acesso se diferente do padrão
                if nivel_acesso != 'visualizacao':
                    conn = Usuario.get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('UPDATE usuarios SET nivel_acesso = ? WHERE id = ?', (nivel_acesso, usuario.id))
                    conn.commit()
                    conn.close()
                    usuario.nivel_acesso = nivel_acesso
                
                return usuario.to_dict(), 201
            except ValueError as e:
                user_ns.abort(400, str(e))
            except Exception as e:
                user_ns.abort(500, f"Erro ao criar usuário: {str(e)}")
    
    @user_ns.route('/<int:id>')
    @user_ns.param('id', 'ID do usuário')
    class UsuarioResource(Resource):
        @user_ns.doc('obter_usuario')
        @user_ns.response(200, 'Sucesso', usuario_resposta_model)
        @user_ns.response(404, 'Usuário não encontrado')
        @require_manager_or_admin
        def get(self, id):
            """Obter usuário por ID"""
            try:
                conn = Usuario.get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM usuarios WHERE id = ?', (id,))
                usuario_data = cursor.fetchone()
                conn.close()
                
                if not usuario_data:
                    user_ns.abort(404, f"Usuário com ID {id} não encontrado")
                
                return {
                    'id': usuario_data[0],
                    'nome': usuario_data[1],
                    'email': usuario_data[2],
                    'nivel_acesso': usuario_data[5],
                    'ativo': bool(usuario_data[6]),
                    'data_criacao': usuario_data[7]
                }
            except Exception as e:
                user_ns.abort(500, f"Erro ao obter usuário: {str(e)}")
        
        @user_ns.doc('atualizar_usuario')
        @user_ns.expect(usuario_update_model)
        @user_ns.response(200, 'Usuário atualizado com sucesso', usuario_resposta_model)
        @user_ns.response(400, 'Erro de validação')
        @user_ns.response(404, 'Usuário não encontrado')
        @require_admin
        def put(self, id):
            """Atualizar usuário (apenas administrativo)"""
            try:
                dados = request.get_json()
                if not dados:
                    user_ns.abort(400, "Dados são obrigatórios")
                
                conn = Usuario.get_db_connection()
                cursor = conn.cursor()
                
                # Verificar se usuário existe
                cursor.execute('SELECT * FROM usuarios WHERE id = ?', (id,))
                usuario_existente = cursor.fetchone()
                
                if not usuario_existente:
                    conn.close()
                    user_ns.abort(404, f"Usuário com ID {id} não encontrado")
                
                # Preparar dados para atualização
                nome = dados.get('nome', usuario_existente[1])
                nivel_acesso = dados.get('nivel_acesso', usuario_existente[5])
                ativo = dados.get('ativo', usuario_existente[6])
                
                if not validar_nivel_acesso(nivel_acesso):
                    conn.close()
                    user_ns.abort(400, "Nível de acesso inválido")
                
                # Atualizar usuário
                cursor.execute('''
                    UPDATE usuarios 
                    SET nome = ?, nivel_acesso = ?, ativo = ?
                    WHERE id = ?
                ''', (nome, nivel_acesso, ativo, id))
                
                conn.commit()
                conn.close()
                
                return {
                    'id': id,
                    'nome': nome,
                    'email': usuario_existente[2],
                    'nivel_acesso': nivel_acesso,
                    'ativo': ativo,
                    'data_criacao': usuario_existente[7]
                }
            except Exception as e:
                user_ns.abort(500, f"Erro ao atualizar usuário: {str(e)}")
        
        @user_ns.doc('remover_usuario')
        @user_ns.response(200, 'Usuário removido com sucesso')
        @user_ns.response(404, 'Usuário não encontrado')
        @require_admin
        def delete(self, id):
            """Remover usuário (apenas administrativo)"""
            try:
                conn = Usuario.get_db_connection()
                cursor = conn.cursor()
                
                # Verificar se usuário existe
                cursor.execute('SELECT * FROM usuarios WHERE id = ?', (id,))
                usuario_existente = cursor.fetchone()
                
                if not usuario_existente:
                    conn.close()
                    user_ns.abort(404, f"Usuário com ID {id} não encontrado")
                
                # Desativar usuário (soft delete)
                cursor.execute('UPDATE usuarios SET ativo = 0 WHERE id = ?', (id,))
                conn.commit()
                conn.close()
                
                return {
                    'message': f'Usuário com ID {id} removido com sucesso',
                    'status': 'sucesso'
                }
            except Exception as e:
                user_ns.abort(500, f"Erro ao remover usuário: {str(e)}")
    
    @user_ns.route('/niveis')
    class NiveisAcesso(Resource):
        @user_ns.doc('listar_niveis')
        @user_ns.response(200, 'Sucesso', niveis_model)
        @require_manager_or_admin
        def get(self):
            """Listar níveis de acesso disponíveis"""
            try:
                return {
                    'niveis': obter_niveis_disponiveis()
                }
            except Exception as e:
                user_ns.abort(500, f"Erro ao listar níveis: {str(e)}")
    
    @user_ns.route('/<int:id>/nivel')
    @user_ns.param('id', 'ID do usuário')
    class AlterarNivel(Resource):
        @user_ns.doc('alterar_nivel_usuario')
        @user_ns.expect(user_ns.model('AlterarNivel', {
            'nivel_acesso': fields.String(required=True, enum=['visualizacao', 'gerencial', 'administrativo'], description='Novo nível de acesso')
        }))
        @user_ns.response(200, 'Nível alterado com sucesso')
        @user_ns.response(400, 'Erro de validação')
        @user_ns.response(404, 'Usuário não encontrado')
        @require_admin
        def put(self, id):
            """Alterar nível de acesso de um usuário (apenas administrativo)"""
            try:
                dados = request.get_json()
                if not dados or 'nivel_acesso' not in dados:
                    user_ns.abort(400, "Campo 'nivel_acesso' é obrigatório")
                
                nivel_acesso = dados['nivel_acesso']
                
                if not validar_nivel_acesso(nivel_acesso):
                    user_ns.abort(400, "Nível de acesso inválido")
                
                conn = Usuario.get_db_connection()
                cursor = conn.cursor()
                
                # Verificar se usuário existe
                cursor.execute('SELECT * FROM usuarios WHERE id = ?', (id,))
                usuario_existente = cursor.fetchone()
                
                if not usuario_existente:
                    conn.close()
                    user_ns.abort(404, f"Usuário com ID {id} não encontrado")
                
                # Atualizar nível de acesso
                cursor.execute('UPDATE usuarios SET nivel_acesso = ? WHERE id = ?', (nivel_acesso, id))
                conn.commit()
                conn.close()
                
                return {
                    'message': f'Nível de acesso do usuário {id} alterado para {nivel_acesso}',
                    'status': 'sucesso'
                }
            except Exception as e:
                user_ns.abort(500, f"Erro ao alterar nível: {str(e)}")
    
    return user_ns
