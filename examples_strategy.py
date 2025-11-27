#!/usr/bin/env python3
"""
Exemplo de uso do padrão Strategy para autorização
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.authorization_strategy import (
    AuthorizationContext,
    VisualizacaoStrategy,
    GerencialStrategy,
    AdministrativoStrategy,
    create_authorization_context
)


def exemplo_uso_strategy():
    """Demonstra o uso do padrão Strategy"""
    
    print("=" * 60)
    print("EXEMPLO: Padrão Strategy para Autorização")
    print("=" * 60)
    print()
    
    # Exemplo 1: Usando o contexto diretamente
    print("1. Criando contexto para usuário com nível 'visualizacao':")
    context_visualizacao = create_authorization_context('visualizacao')
    print(f"   Nível: {context_visualizacao.get_level_name()}")
    print(f"   Pode criar tarefa? {context_visualizacao.can_perform_action('tarefas:create')}")
    print(f"   Pode ler tarefa? {context_visualizacao.can_perform_action('tarefas:read')}")
    print(f"   Ações permitidas: {context_visualizacao.get_allowed_actions()}")
    print()
    
    # Exemplo 2: Usando estratégia gerencial
    print("2. Criando contexto para usuário com nível 'gerencial':")
    context_gerencial = create_authorization_context('gerencial')
    print(f"   Nível: {context_gerencial.get_level_name()}")
    print(f"   Pode criar tarefa? {context_gerencial.can_perform_action('tarefas:create')}")
    print(f"   Pode deletar tarefa? {context_gerencial.can_perform_action('tarefas:delete')}")
    print(f"   Pode criar usuário? {context_gerencial.can_perform_action('usuarios:create')}")
    print()
    
    # Exemplo 3: Usando estratégia administrativa
    print("3. Criando contexto para usuário com nível 'administrativo':")
    context_admin = create_authorization_context('administrativo')
    print(f"   Nível: {context_admin.get_level_name()}")
    print(f"   Pode criar tarefa? {context_admin.can_perform_action('tarefas:create')}")
    print(f"   Pode criar usuário? {context_admin.can_perform_action('usuarios:create')}")
    print(f"   Pode acessar admin? {context_admin.can_perform_action('system:admin')}")
    print()
    
    # Exemplo 4: Usando estratégias diretamente (sem contexto)
    print("4. Usando estratégias diretamente:")
    strategy_visual = VisualizacaoStrategy()
    print(f"   Estratégia: {strategy_visual.get_level_name()}")
    print(f"   Ações: {strategy_visual.get_allowed_actions()}")
    print()
    
    # Exemplo 5: Comparando diferentes estratégias
    print("5. Comparação de permissões entre níveis:")
    acoes = ['tarefas:read', 'tarefas:create', 'tarefas:delete', 'usuarios:create']
    
    niveis = ['visualizacao', 'gerencial', 'administrativo']
    for nivel in niveis:
        context = create_authorization_context(nivel)
        print(f"   {nivel.upper()}:")
        for acao in acoes:
            pode = context.can_perform_action(acao)
            status = "✓" if pode else "✗"
            print(f"     {status} {acao}")
    print()
    
    print("=" * 60)
    print("VANTAGENS DO PADRÃO STRATEGY:")
    print("=" * 60)
    print("• Cada nível de acesso tem sua própria estratégia")
    print("• Fácil adicionar novos níveis sem modificar código existente")
    print("• Lógica de autorização isolada e testável")
    print("• Permite trocar estratégia em tempo de execução")
    print("=" * 60)


if __name__ == '__main__':
    exemplo_uso_strategy()

