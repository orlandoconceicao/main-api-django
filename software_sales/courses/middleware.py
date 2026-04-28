import threading

_thread_locals = threading.local()


def get_current_user():
    return getattr(_thread_locals, "user", None)


class AuditoriaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            _thread_locals.user = getattr(request, "user", None)
        except Exception:
            _thread_locals.user = None

        response = self.get_response(request)

        _thread_locals.user = None
        return response