from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status as http_status
from http.client import responses  # Importa as descrições de status HTTP

def custom_exception_handler(exc, context):
    # Chama o manipulador padrão de exceções do DRF
    response = exception_handler(exc, context)

    # Inicializa o corpo da resposta
    data = {
        'message': '',
        'status': None,
        'error': '',
        'cause': exc.__class__.__name__,  # Classe da exceção como causa
        'errors': {}
    }

    # Cria uma resposta padrão caso o response seja None
    if response is None:
        data['message'] = 'Erro desconhecido'
        data['status'] = http_status.HTTP_500_INTERNAL_SERVER_ERROR
        data['error'] = 'Internal Server Error'
        data['errors'] = str(exc)  # Captura a exceção como string

        return Response(data, status=data['status'])

    # Verifica se a exceção é do tipo ValidationError
    if isinstance(exc, ValidationError):
        data['message'] = 'Erro de validação'
        data['status'] = http_status.HTTP_400_BAD_REQUEST
        data['error'] = 'Bad Request'
        data['errors'] = response.data  # Lista de erros específicos

    else:
        # Tratamento para exceções gerais
        data['message'] = response.data.get('detail', 'Erro desconhecido')
        data['status'] = response.status_code
        data['error'] = responses.get(response.status_code, 'Erro desconhecido')
        data['errors'] = response.data  # Pega os dados de erro padrão do DRF

    return Response(data, status=data['status'])
