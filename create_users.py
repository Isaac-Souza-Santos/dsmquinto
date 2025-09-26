#!/usr/bin/env python3
"""
Script para criar usuários de exemplo com diferentes níveis de acesso
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models.usuario import Usuario, init_auth_database
import sqlite3

def create_example_users():
    """Cria usuários de exemplo com diferentes níveis de acesso"""
    
    # Inicializar banco de dados
    init_auth_database()
    
    # Usuários de exemplo
    usuarios_exemplo = [
        {
            'nome': 'Administrador Sistema',
            'email': 'admin@dpm.com',
            'senha': 'admin123',
            'nivel_acesso': 'administrativo'
        },
        {
            'nome': 'Gerente Projetos',
            'email': 'gerente@dpm.com',
            'senha': 'gerente123',
            'nivel_acesso': 'gerencial'
        },
        {
            'nome': 'Visualizador Dados',
            'email': 'visualizador@dpm.com',
            'senha': 'visual123',
            'nivel_acesso': 'visualizacao'
        }
    ]
    
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    
    print("🚀 Criando usuários de exemplo...")
    
    for usuario_data in usuarios_exemplo:
        try:
            # Verificar se usuário já existe
            cursor.execute('SELECT id FROM usuarios WHERE email = ?', (usuario_data['email'],))
            if cursor.fetchone():
                print(f"⚠️  Usuário {usuario_data['email']} já existe, pulando...")
                continue
            
            # Criar usuário
            usuario = Usuario.criar(
                usuario_data['nome'],
                usuario_data['email'],
                usuario_data['senha']
            )
            
            # Atualizar nível de acesso
            cursor.execute('UPDATE usuarios SET nivel_acesso = ? WHERE id = ?', 
                         (usuario_data['nivel_acesso'], usuario.id))
            
            print(f"✅ Usuário criado: {usuario_data['nome']} ({usuario_data['nivel_acesso']})")
            print(f"   Email: {usuario_data['email']}")
            print(f"   Senha: {usuario_data['senha']}")
            print()
            
        except Exception as e:
            print(f"❌ Erro ao criar usuário {usuario_data['email']}: {str(e)}")
    
    conn.commit()
    conn.close()
    
    print("🎉 Usuários de exemplo criados com sucesso!")
    print("\n📋 Resumo dos usuários:")
    print("1. Administrador (admin@dpm.com) - Acesso total")
    print("2. Gerente (gerente@dpm.com) - Gerenciar tarefas e usuários")
    print("3. Visualizador (visualizador@dpm.com) - Apenas visualizar")
    print("\n🔐 Use estes usuários para testar os diferentes níveis de acesso!")

if __name__ == '__main__':
    create_example_users()
