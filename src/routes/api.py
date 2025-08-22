from flask import request
from flask_restx import Resource, Namespace
from datetime import datetime

def create_routes(api):
    """Cria as rotas da API de tarefas"""
    
    # Namespace para organizar as rotas
    api_ns = Namespace('tarefas', description='Operações CRUD para tarefas')
    
    # Criar modelos
    from src.models.tarefa import create_models, init_database, get_db_connection
    tarefa_model, tarefa_resposta_model, tarefa_lista_model, mensagem_model = create_models(api)
    
    # Inicializar banco de dados
    init_database()
    
    @api_ns.route('/')
    class TarefasList(Resource):
        @api_ns.doc('listar_tarefas')
        @api_ns.response(200, 'Sucesso', tarefa_lista_model)
        def get(self):
            """Listar todas as tarefas"""
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM tarefas ORDER BY data_criacao DESC')
                tarefas = cursor.fetchall()
                
                tarefas_list = []
                for tarefa in tarefas:
                    tarefas_list.append({
                        'id': tarefa[0],
                        'titulo': tarefa[1],
                        'descricao': tarefa[2],
                        'status': tarefa[3],
                        'data_criacao': tarefa[4],
                        'data_atualizacao': tarefa[5]
                    })
                
                conn.close()
                
                return {
                    'tarefas': tarefas_list,
                    'total': len(tarefas_list)
                }
            except Exception as e:
                api_ns.abort(500, f"Erro ao listar tarefas: {str(e)}")
        
        @api_ns.doc('criar_tarefa')
        @api_ns.expect(tarefa_model)
        @api_ns.response(201, 'Tarefa criada com sucesso', tarefa_resposta_model)
        @api_ns.response(400, 'Erro de validação')
        def post(self):
            """Criar nova tarefa"""
            try:
                dados = request.get_json()
                if not dados or 'titulo' not in dados:
                    api_ns.abort(400, "Campo 'titulo' é obrigatório")
                
                titulo = dados['titulo']
                descricao = dados.get('descricao', '')
                status = dados.get('status', 'pendente')
                
                if status not in ['pendente', 'concluida']:
                    api_ns.abort(400, "Status deve ser 'pendente' ou 'concluida'")
                
                data_atual = datetime.now().isoformat()
                
                conn = get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO tarefas (titulo, descricao, status, data_criacao, data_atualizacao)
                    VALUES (?, ?, ?, ?, ?)
                ''', (titulo, descricao, status, data_atual, data_atual))
                
                tarefa_id = cursor.lastrowid
                conn.commit()
                conn.close()
                
                return {
                    'id': tarefa_id,
                    'titulo': titulo,
                    'descricao': descricao,
                    'status': status,
                    'data_criacao': data_atual,
                    'data_atualizacao': data_atual
                }, 201
            except Exception as e:
                api_ns.abort(500, f"Erro ao criar tarefa: {str(e)}")
    
    @api_ns.route('/<int:id>')
    @api_ns.param('id', 'ID da tarefa')
    class Tarefa(Resource):
        @api_ns.doc('obter_tarefa')
        @api_ns.response(200, 'Sucesso', tarefa_resposta_model)
        @api_ns.response(404, 'Tarefa não encontrada')
        def get(self, id):
            """Obter tarefa por ID"""
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM tarefas WHERE id = ?', (id,))
                tarefa = cursor.fetchone()
                
                conn.close()
                
                if not tarefa:
                    api_ns.abort(404, f"Tarefa com ID {id} não encontrada")
                
                return {
                    'id': tarefa[0],
                    'titulo': tarefa[1],
                    'descricao': tarefa[2],
                    'status': tarefa[3],
                    'data_criacao': tarefa[4],
                    'data_atualizacao': tarefa[5]
                }
            except Exception as e:
                api_ns.abort(500, f"Erro ao obter tarefa: {str(e)}")
        
        @api_ns.doc('atualizar_tarefa')
        @api_ns.expect(tarefa_model)
        @api_ns.response(200, 'Tarefa atualizada com sucesso', tarefa_resposta_model)
        @api_ns.response(400, 'Erro de validação')
        @api_ns.response(404, 'Tarefa não encontrada')
        def put(self, id):
            """Atualizar tarefa por ID"""
            try:
                dados = request.get_json()
                if not dados:
                    api_ns.abort(400, "Dados são obrigatórios")
                
                conn = get_db_connection()
                cursor = conn.cursor()
                
                # Verificar se a tarefa existe
                cursor.execute('SELECT * FROM tarefas WHERE id = ?', (id,))
                tarefa_existente = cursor.fetchone()
                
                if not tarefa_existente:
                    conn.close()
                    api_ns.abort(404, f"Tarefa com ID {id} não encontrada")
                
                # Preparar dados para atualização
                titulo = dados.get('titulo', tarefa_existente[1])
                descricao = dados.get('descricao', tarefa_existente[2])
                status = dados.get('status', tarefa_existente[3])
                
                if status not in ['pendente', 'concluida']:
                    conn.close()
                    api_ns.abort(400, "Status deve ser 'pendente' ou 'concluida'")
                
                data_atual = datetime.now().isoformat()
                
                cursor.execute('''
                    UPDATE tarefas 
                    SET titulo = ?, descricao = ?, status = ?, data_atualizacao = ?
                    WHERE id = ?
                ''', (titulo, descricao, status, data_atual, id))
                
                conn.commit()
                conn.close()
                
                return {
                    'id': id,
                    'titulo': titulo,
                    'descricao': descricao,
                    'status': status,
                    'data_criacao': tarefa_existente[4],
                    'data_atualizacao': data_atual
                }
            except Exception as e:
                api_ns.abort(500, f"Erro ao atualizar tarefa: {str(e)}")
        
        @api_ns.doc('remover_tarefa')
        @api_ns.response(200, 'Tarefa removida com sucesso', mensagem_model)
        @api_ns.response(404, 'Tarefa não encontrada')
        def delete(self, id):
            """Remover tarefa por ID"""
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                
                # Verificar se a tarefa existe
                cursor.execute('SELECT * FROM tarefas WHERE id = ?', (id,))
                tarefa_existente = cursor.fetchone()
                
                if not tarefa_existente:
                    conn.close()
                    api_ns.abort(404, f"Tarefa com ID {id} não encontrada")
                
                cursor.execute('DELETE FROM tarefas WHERE id = ?', (id,))
                conn.commit()
                conn.close()
                
                return {
                    'message': f'Tarefa com ID {id} removida com sucesso',
                    'status': 'sucesso'
                }
            except Exception as e:
                api_ns.abort(500, f"Erro ao remover tarefa: {str(e)}")
    
    return api_ns
