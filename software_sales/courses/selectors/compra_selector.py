from courses.models import Compra


def listar_compras_usuario(usuario):
    return Compra.objects.select_related(
        "usuario",
        "curso",
    ).filter(usuario=usuario)