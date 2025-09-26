#!/usr/bin/env python3
"""
Script para atualizar a estrutura do banco de dados
"""

import sqlite3
import os

def update_database():
    """Atualiza a estrutura do banco de dados"""
    
    db_path = 'tarefas.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔄 Atualizando estrutura do banco de dados...")
    
    try:
        # Verificar se a coluna nivel_acesso existe
        cursor.execute("PRAGMA table_info(usuarios)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'nivel_acesso' not in columns:
            print("➕ Adicionando coluna nivel_acesso...")
            cursor.execute('ALTER TABLE usuarios ADD COLUMN nivel_acesso TEXT DEFAULT "visualizacao"')
            print("✅ Coluna nivel_acesso adicionada")
        else:
            print("✅ Coluna nivel_acesso já existe")
        
        # Verificar se a coluna usuario_id existe na tabela tarefas
        cursor.execute("PRAGMA table_info(tarefas)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'usuario_id' not in columns:
            print("➕ Adicionando coluna usuario_id na tabela tarefas...")
            cursor.execute('ALTER TABLE tarefas ADD COLUMN usuario_id INTEGER')
            print("✅ Coluna usuario_id adicionada")
        else:
            print("✅ Coluna usuario_id já existe")
        
        conn.commit()
        print("🎉 Banco de dados atualizado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao atualizar banco: {str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
    update_database()
