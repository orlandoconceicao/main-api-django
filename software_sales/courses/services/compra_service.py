from django.db import transaction

from software_sales.courses.models import Compra, CompraStatus


@transaction.atomic
def criar_compra(*, usuario, curso):
    return Compra.objects.create(
        usuario=usuario,
        curso=curso,
        preco=curso.preco,
        status=CompraStatus.COMPLETED,
    )


@transaction.atomic
def aprovar_reembolso(*, compra):
    compra.status = CompraStatus.REFUNDED
    compra.save(update_fields=["status"])
    return compra
