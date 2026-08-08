from software_sales.courses.models import Avaliacao


def criar_avaliacao(*, usuario, curso, nota, comentario=""):
    return Avaliacao.objects.create(
        usuario=usuario,
        curso=curso,
        nota=nota,
        comentario=comentario,
    )
