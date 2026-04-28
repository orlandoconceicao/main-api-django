from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(response.data, dict):
            response.data = {
                "success": False,
                "error": response.data
            }

        elif isinstance(response.data, list):
            response.data = {
                "success": False,
                "error": response.data[0]
            }

    return response