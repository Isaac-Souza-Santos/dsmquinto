"""
Sistema de Permissões e Níveis de Acesso
"""

# Níveis de acesso disponíveis
NIVEIS_ACESSO = {
    'visualizacao': {
        'nome': 'Visualização',
        'descricao': 'Apenas visualizar dados',
        'nivel': 1,
        'permissoes': [
            'tarefas:read',
            'tarefas:list'
        ]
    },
    'gerencial': {
        'nome': 'Gerencial',
        'descricao': 'Gerenciar tarefas e usuários',
        'nivel': 2,
        'permissoes': [
            'tarefas:read',
            'tarefas:list',
            'tarefas:create',
            'tarefas:update',
            'tarefas:delete',
            'usuarios:read',
            'usuarios:list'
        ]
    },
    'administrativo': {
        'nome': 'Administrativo',
        'descricao': 'Acesso total ao sistema',
        'nivel': 3,
        'permissoes': [
            'tarefas:read',
            'tarefas:list',
            'tarefas:create',
            'tarefas:update',
            'tarefas:delete',
            'usuarios:read',
            'usuarios:list',
            'usuarios:create',
            'usuarios:update',
            'usuarios:delete',
            'usuarios:change_role',
            'system:admin'
        ]
    }
}

def verificar_permissao(nivel_usuario, permissao_necessaria):
    """
    Verifica se um usuário tem permissão para uma ação específica
    
    Args:
        nivel_usuario (str): Nível de acesso do usuário
        permissao_necessaria (str): Permissão necessária para a ação
    
    Returns:
        bool: True se tem permissão, False caso contrário
    """
    if nivel_usuario not in NIVEIS_ACESSO:
        return False
    
    return permissao_necessaria in NIVEIS_ACESSO[nivel_usuario]['permissoes']

def verificar_nivel_minimo(nivel_usuario, nivel_minimo):
    """
    Verifica se o usuário tem nível mínimo necessário
    
    Args:
        nivel_usuario (str): Nível de acesso do usuário
        nivel_minimo (str): Nível mínimo necessário
    
    Returns:
        bool: True se tem nível suficiente, False caso contrário
    """
    if nivel_usuario not in NIVEIS_ACESSO or nivel_minimo not in NIVEIS_ACESSO:
        return False
    
    return NIVEIS_ACESSO[nivel_usuario]['nivel'] >= NIVEIS_ACESSO[nivel_minimo]['nivel']

def obter_permissoes_usuario(nivel_usuario):
    """
    Retorna todas as permissões de um usuário
    
    Args:
        nivel_usuario (str): Nível de acesso do usuário
    
    Returns:
        list: Lista de permissões do usuário
    """
    if nivel_usuario not in NIVEIS_ACESSO:
        return []
    
    return NIVEIS_ACESSO[nivel_usuario]['permissoes']

def obter_niveis_disponiveis():
    """
    Retorna todos os níveis de acesso disponíveis
    
    Returns:
        dict: Dicionário com todos os níveis de acesso
    """
    return NIVEIS_ACESSO

def validar_nivel_acesso(nivel):
    """
    Valida se um nível de acesso é válido
    
    Args:
        nivel (str): Nível de acesso a validar
    
    Returns:
        bool: True se válido, False caso contrário
    """
    return nivel in NIVEIS_ACESSO
