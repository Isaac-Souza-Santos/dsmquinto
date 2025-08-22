#!/usr/bin/env python3
"""
Exemplos de uso da API de Tarefas
Este arquivo demonstra como usar todas as rotas da API
"""

import requests
import json

# Configuração da API
BASE_URL = "http://localhost:5000"
API_URL = f"{BASE_URL}/tarefas"

def print_response(response, operation):
    """Imprime a resposta de uma operação"""
    print(f"\n{'='*50}")
    print(f"🔍 {operation}")
    print(f"📊 Status: {response.status_code}")
    print(f"📝 Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print(f"{'='*50}")

def test_api():
    """Testa todas as operações da API"""
    print("🚀 Testando API de Tarefas")
    print(f"📍 URL Base: {BASE_URL}")
    print(f"📚 Swagger: {BASE_URL}/docs")
    
    # 1. Listar tarefas (inicialmente vazio)
    print("\n1️⃣ Listando tarefas existentes...")
    response = requests.get(API_URL)
    print_response(response, "Listar Tarefas")
    
    # 2. Criar primeira tarefa
    print("\n2️⃣ Criando primeira tarefa...")
    tarefa1 = {
        "titulo": "Estudar Python",
        "descricao": "Revisar conceitos básicos de Python e Flask",
        "status": "pendente"
    }
    response = requests.post(API_URL, json=tarefa1)
    print_response(response, "Criar Tarefa 1")
    
    if response.status_code == 201:
        tarefa1_id = response.json()['id']
        print(f"✅ Tarefa criada com ID: {tarefa1_id}")
    
    # 3. Criar segunda tarefa
    print("\n3️⃣ Criando segunda tarefa...")
    tarefa2 = {
        "titulo": "Implementar API REST",
        "descricao": "Criar endpoints para operações CRUD",
        "status": "pendente"
    }
    response = requests.post(API_URL, json=tarefa2)
    print_response(response, "Criar Tarefa 2")
    
    if response.status_code == 201:
        tarefa2_id = response.json()['id']
        print(f"✅ Tarefa criada com ID: {tarefa2_id}")
    
    # 4. Listar todas as tarefas
    print("\n4️⃣ Listando todas as tarefas...")
    response = requests.get(API_URL)
    print_response(response, "Listar Todas as Tarefas")
    
    # 5. Obter tarefa específica
    if 'tarefa1_id' in locals():
        print(f"\n5️⃣ Obtendo tarefa com ID {tarefa1_id}...")
        response = requests.get(f"{API_URL}/{tarefa1_id}")
        print_response(response, f"Obter Tarefa {tarefa1_id}")
    
    # 6. Atualizar tarefa
    if 'tarefa1_id' in locals():
        print(f"\n6️⃣ Atualizando tarefa com ID {tarefa1_id}...")
        atualizacao = {
            "status": "concluida",
            "descricao": "Concluído: Revisar conceitos básicos de Python e Flask"
        }
        response = requests.put(f"{API_URL}/{tarefa1_id}", json=atualizacao)
        print_response(response, f"Atualizar Tarefa {tarefa1_id}")
    
    # 7. Listar tarefas após atualização
    print("\n7️⃣ Listando tarefas após atualização...")
    response = requests.get(API_URL)
    print_response(response, "Listar Tarefas Atualizadas")
    
    # 8. Remover tarefa
    if 'tarefa2_id' in locals():
        print(f"\n8️⃣ Removendo tarefa com ID {tarefa2_id}...")
        response = requests.delete(f"{API_URL}/{tarefa2_id}")
        print_response(response, f"Remover Tarefa {tarefa2_id}")
    
    # 9. Listar tarefas finais
    print("\n9️⃣ Listando tarefas finais...")
    response = requests.get(API_URL)
    print_response(response, "Listar Tarefas Finais")
    
    print("\n🎉 Teste da API concluído!")
    print(f"📚 Acesse {BASE_URL}/docs para mais informações")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API")
        print("💡 Certifique-se de que a API está rodando em http://localhost:5000")
        print("🚀 Execute: python main.py")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
