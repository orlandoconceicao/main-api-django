from decimal import Decimal
from django.db.models import Avg

from courses.models import Avaliacao


def criar_avaliacao(*, usuario, curso, nota, comentario=""):
    avaliacao = Avaliacao.objects.create(
        usuario=usuario,
        curso=curso,
        nota=nota,
        comentario=comentario,
    )

    atualizar_media_curso(curso)

    return avaliacao


def atualizar_media_curso(curso):
    media = curso.avaliacoes.aggregate(
        media=Avg("nota")
    )["media"] or Decimal("0.00")

    curso.media_avaliacoes = round(media, 2)

    curso.save(update_fields=["media_avaliacoes"])