# courses/exceptions.py

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        erros = response.data

        # erro de validação de campo
        if isinstance(erros, dict):
            for campo, mensagem in erros.items():
                if isinstance(mensagem, list):
                    mensagem = mensagem[0]

                response.data = {
                    "campo": campo,
                    "erro": str(mensagem)
                }
                break

        # erro geral
        elif isinstance(erros, list):
            response.data = {
                "erro": str(erros[0])
            }

    return response