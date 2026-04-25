import threading
from django.db import connection

_thread_locals = threading.local()


def get_current_user():
    return getattr(_thread_locals, "user", None)


class AuditoriaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 🔒 evita rodar em requests internas do Django (migrate, celery, etc.)
        if self._is_internal_request(request):
            return self.get_response(request)

        try:
            # salva usuário no contexto da thread
            _thread_locals.user = getattr(request, "user", None)

            response = self.get_response(request)
            return response

        finally:
            # limpa sempre a thread (evita vazamento de memória/contexto)
            _thread_locals.user = None

    def _is_internal_request(self, request):
        """
        Evita auditoria durante:
        - migrations
        - celery tasks
        - system checks
        """

        # 1. Sem request válido
        if not request:
            return True

        # 2. Durante startup/migrate pode não existir META corretamente
        if not hasattr(request, "path"):
            return True

        # 3. evita rotas internas do Django admin/migrate/health checks
        internal_paths = [
            "/admin",
            "/static",
            "/__debug__",
        ]

        if any(request.path.startswith(p) for p in internal_paths):
            return True

        # 4. evita erro durante migrações (ESSENCIAL pro seu caso)
        try:
            if "django_migrations" not in connection.introspection.table_names():
                return True
        except Exception:
            return True

        return False