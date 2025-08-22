from src.api.app import create_app

if __name__ == '__main__':
    # Criar aplicação
    app, api = create_app()
    
    print("🚀 API de Tarefas iniciando...")
    print("📍 Acesse: http://localhost:5000")
    print("📚 Swagger: http://localhost:5000/docs")
    print("✅ CRUD completo implementado!")
    print("🗄️  Banco SQLite configurado automaticamente")
    
    # Executar aplicação
    app.run(host='0.0.0.0', port=5000, debug=True)
