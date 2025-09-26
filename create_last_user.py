#!/usr/bin/env python3
"""
Script para criar o último usuário
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models.usuario import Usuario
import sqlite3

def create_last_user():
    """Cria o último usuário de exemplo"""
    
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    
    try:
        # Criar usuário visualizador
        usuario = Usuario.criar(
            'Visualizador Dados',
            'visualizador@dpm.com',
            'visual123'
        )
        
        # Atualizar nível de acesso
        cursor.execute('UPDATE usuarios SET nivel_acesso = ? WHERE id = ?', 
                     ('visualizacao', usuario.id))
        
        print(f"✅ Usuário criado: Visualizador Dados (visualizacao)")
        print(f"   Email: visualizador@dpm.com")
        print(f"   Senha: visual123")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    finally:
        conn.commit()
        conn.close()

if __name__ == '__main__':
    create_last_user()
