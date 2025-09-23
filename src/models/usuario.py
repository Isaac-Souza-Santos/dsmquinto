from flask_restx import fields
import sqlite3
import os
import pyotp
import qrcode
from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

def create_auth_models(api):
    """Cria os modelos para autenticação no Swagger"""
    
    # Modelo para registro de usuário
    usuario_registro_model = api.model('UsuarioRegistro', {
        'nome': fields.String(required=True, description='Nome completo do usuário'),
        'email': fields.String(required=True, description='Email do usuário'),
        'senha': fields.String(required=True, description='Senha do usuário', min_length=6)
    })
    
    # Modelo para login
    usuario_login_model = api.model('UsuarioLogin', {
        'email': fields.String(required=True, description='Email do usuário'),
        'senha': fields.String(required=True, description='Senha do usuário')
    })
    
    # Modelo para verificação 2FA
    verificar_2fa_model = api.model('Verificar2FA', {
        'codigo': fields.String(required=True, description='Código de 6 dígitos do Google Authenticator')
    })
    
    # Modelo para resposta de usuário
    usuario_resposta_model = api.model('UsuarioResposta', {
        'id': fields.Integer(description='ID do usuário'),
        'nome': fields.String(description='Nome do usuário'),
        'email': fields.String(description='Email do usuário'),
        '2fa_ativo': fields.Boolean(description='2FA ativado'),
        'data_criacao': fields.String(description='Data de criação')
    })
    
    # Modelo para resposta de login
    login_resposta_model = api.model('LoginResposta', {
        'usuario': fields.Nested(usuario_resposta_model),
        'token': fields.String(description='JWT Token'),
        '2fa_necessario': fields.Boolean(description='2FA necessário'),
        'qr_code_url': fields.String(description='URL do QR Code para 2FA')
    })
    
    return usuario_registro_model, usuario_login_model, verificar_2fa_model, usuario_resposta_model, login_resposta_model

def init_auth_database():
    """Inicializa as tabelas de autenticação"""
    db_path = 'tarefas.db'
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            secret_2fa TEXT,
            ativo BOOLEAN DEFAULT 1,
            data_criacao TEXT NOT NULL
        )
    ''')
    
    # Tabela de sessões JWT
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TEXT NOT NULL,
            ativo BOOLEAN DEFAULT 1,
            data_criacao TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    
    # Adicionar coluna usuario_id na tabela tarefas se não existir
    try:
        cursor.execute('ALTER TABLE tarefas ADD COLUMN usuario_id INTEGER')
    except sqlite3.OperationalError:
        pass  # Coluna já existe
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Retorna uma conexão com o banco de dados"""
    return sqlite3.connect('tarefas.db')

class Usuario:
    def __init__(self, id=None, nome=None, email=None, senha_hash=None, secret_2fa=None, ativo=True, data_criacao=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.secret_2fa = secret_2fa
        self.ativo = ativo
        self.data_criacao = data_criacao
    
    @staticmethod
    def criar(nome, email, senha):
        """Cria um novo usuário"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar se email já existe
        cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            raise ValueError("Email já cadastrado")
        
        # Gerar hash da senha
        senha_hash = generate_password_hash(senha)
        
        # Gerar secret para 2FA
        secret_2fa = pyotp.random_base32()
        
        data_atual = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO usuarios (nome, email, senha_hash, secret_2fa, data_criacao)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, email, senha_hash, secret_2fa, data_atual))
        
        usuario_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return Usuario(id=usuario_id, nome=nome, email=email, secret_2fa=secret_2fa, data_criacao=data_atual)
    
    @staticmethod
    def buscar_por_email(email):
        """Busca usuário por email"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM usuarios WHERE email = ? AND ativo = 1', (email,))
        usuario_data = cursor.fetchone()
        conn.close()
        
        if not usuario_data:
            return None
        
        return Usuario(
            id=usuario_data[0],
            nome=usuario_data[1],
            email=usuario_data[2],
            senha_hash=usuario_data[3],
            secret_2fa=usuario_data[4],
            ativo=usuario_data[5],
            data_criacao=usuario_data[6]
        )
    
    def verificar_senha(self, senha):
        """Verifica se a senha está correta"""
        return check_password_hash(self.senha_hash, senha)
    
    def gerar_qr_code_2fa(self):
        """Gera QR Code para configuração do Google Authenticator"""
        if not self.secret_2fa:
            return None
        
        totp = pyotp.TOTP(self.secret_2fa)
        provisioning_uri = totp.provisioning_uri(
            name=self.email,
            issuer_name="DPM Task Manager"
        )
        
        # Gerar QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        # Salvar QR Code
        qr_dir = "static/qr_codes"
        os.makedirs(qr_dir, exist_ok=True)
        qr_path = f"{qr_dir}/qr_{self.id}.png"
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_path)
        
        return f"/static/qr_codes/qr_{self.id}.png"
    
    def verificar_codigo_2fa(self, codigo):
        """Verifica código do Google Authenticator"""
        if not self.secret_2fa:
            return False
        
        totp = pyotp.TOTP(self.secret_2fa)
        return totp.verify(codigo)
    
    def gerar_jwt_token(self):
        """Gera JWT token para o usuário"""
        payload = {
            'user_id': self.id,
            'email': self.email,
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        
        # Usar secret do config ou padrão
        secret = os.environ.get('JWT_SECRET', 'dev-secret-key')
        token = jwt.encode(payload, secret, algorithm='HS256')
        
        # Salvar token na sessão
        conn = get_db_connection()
        cursor = conn.cursor()
        
        expires_at = (datetime.utcnow() + timedelta(days=7)).isoformat()
        data_atual = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO sessoes (usuario_id, token, expires_at, data_criacao)
            VALUES (?, ?, ?, ?)
        ''', (self.id, token, expires_at, data_atual))
        
        conn.commit()
        conn.close()
        
        return token
    
    @staticmethod
    def verificar_jwt_token(token):
        """Verifica e retorna usuário do JWT token"""
        try:
            secret = os.environ.get('JWT_SECRET', 'dev-secret-key')
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            
            # Verificar se token está ativo no banco
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT s.*, u.* FROM sessoes s
                JOIN usuarios u ON s.usuario_id = u.id
                WHERE s.token = ? AND s.ativo = 1 AND s.expires_at > ?
            ''', (token, datetime.now().isoformat()))
            
            sessao_data = cursor.fetchone()
            conn.close()
            
            if not sessao_data:
                return None
            
            return Usuario(
                id=sessao_data[6],
                nome=sessao_data[7],
                email=sessao_data[8],
                secret_2fa=sessao_data[10],
                ativo=sessao_data[11],
                data_criacao=sessao_data[12]
            )
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def to_dict(self):
        """Converte usuário para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            '2fa_ativo': bool(self.secret_2fa),
            'data_criacao': self.data_criacao
        }
