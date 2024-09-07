from rest_framework.views import exception_handler  # Importa o manipulador padrão de exceções do DRF
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    # Chama o manipulador padrão de exceções do DRF
    response = exception_handler(exc, context)
    
    # Cria uma resposta padrão caso o response seja None
    if response is None:
        response = Response({
            'message': 'Erro desconhecido',
            'errors': str(exc)
        }, status=500)
    
    data = {}
    
    # Verifica se a exceção é do tipo ValidationError
    if isinstance(exc, ValidationError):
        data['message'] = 'Erro de validação'
        # Adiciona os erros originais da resposta
        data['errors'] = response.data
    else:
        data['message'] = response.data.get('detail', 'Erro desconhecido')
    
    return Response(data, status=response.status_code)
