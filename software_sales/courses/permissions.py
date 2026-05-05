from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Compra, CompraStatus


# ADMIN OU SOMENTE LEITURA
class IsAdminOrReadOnly(BasePermission):
    """
    Permite leitura para todos.
    Escrita apenas para admin (is_staff).
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )


# DONO DO OBJETO
class IsOwner(BasePermission):
    """
    Permite acesso apenas ao dono do objeto.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        return obj.usuario == request.user


# USUÁRIO COMPRADOR DO CURSO
class HasPurchasedCourse(BasePermission):
    """
    Permite apenas usuários que compraram o curso.
    """

    message = "Você precisa comprar este curso."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        curso_id = (
            request.data.get("curso_id")
            or request.query_params.get("curso_id")
            or view.kwargs.get("curso_id")
            or view.kwargs.get("pk")
        )

        if not curso_id:
            self.message = "curso_id não informado."
            return False

        return Compra.objects.filter(
            usuario_id=request.user.id,
            curso_id=curso_id,
            status=CompraStatus.COMPLETED
        ).exists()