from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        erros = response.data

        if isinstance(erros, dict):
            for campo, mensagem in erros.items():
                if isinstance(mensagem, list):
                    mensagem = mensagem[0]

                # trata non_field_errors melhor
                if campo == "non_field_errors":
                    response.data = {
                        "success": False,
                        "error": str(mensagem)
                    }
                else:
                    response.data = {
                        "success": False,
                        "campo": campo,
                        "error": str(mensagem)
                    }
                break

        elif isinstance(erros, list):
            response.data = {
                "success": False,
                "error": str(erros[0])
            }

    return response