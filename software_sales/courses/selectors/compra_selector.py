from ..models import Compra


def listar_compras_usuario(usuario):
    if not usuario or not getattr(usuario, "is_authenticated", False):
        return Compra.objects.none()

    return Compra.objects.filter(usuario=usuario)