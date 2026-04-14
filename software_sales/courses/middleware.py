import threading

_thread_locals = threading.local()


class AuditoriaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            _thread_locals.user = getattr(request, "user", None)

            response = self.get_response(request)
            return response

        finally:
            # limpa o contexto após a request
            _thread_locals.user = None