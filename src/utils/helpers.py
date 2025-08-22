import json
from datetime import datetime

def format_response(message, status="sucesso", data=None):
    """Formata resposta padrão da API"""
    response = {
        "message": message,
        "status": status,
        "timestamp": datetime.now().isoformat()
    }
    
    if data:
        response["data"] = data
    
    return response

def validate_json(data):
    """Valida se os dados são JSON válido"""
    try:
        if isinstance(data, str):
            json.loads(data)
        return True
    except (json.JSONDecodeError, TypeError):
        return False
