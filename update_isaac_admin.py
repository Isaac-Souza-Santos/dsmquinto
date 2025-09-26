#!/usr/bin/env python3
"""
Script para alterar o nível de acesso do usuário Isaac para administrativo
"""

import sqlite3

def update_isaac_to_admin():
    """Altera o nível de acesso do Isaac para administrativo"""
    
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    
    try:
        # Verificar se o usuário Isaac existe
        cursor.execute('SELECT id, nome, email, nivel_acesso FROM usuarios WHERE nome LIKE ?', ('%Isaac%',))
        usuario = cursor.fetchone()
        
        if usuario:
            print(f"✅ Usuário encontrado: {usuario[1]} ({usuario[2]})")
            print(f"   Nível atual: {usuario[3]}")
            
            # Atualizar para administrativo
            cursor.execute('UPDATE usuarios SET nivel_acesso = ? WHERE id = ?', ('administrativo', usuario[0]))
            conn.commit()
            
            print(f"✅ Nível alterado para: administrativo")
            print(f"   Usuário {usuario[1]} agora tem acesso administrativo!")
            
        else:
            print("❌ Usuário Isaac não encontrado no banco de dados")
            print("📋 Usuários disponíveis:")
            
            # Listar todos os usuários
            cursor.execute('SELECT id, nome, email, nivel_acesso FROM usuarios')
            usuarios = cursor.fetchall()
            
            for user in usuarios:
                print(f"   - {user[1]} ({user[2]}) - {user[3]}")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
    update_isaac_to_admin()
