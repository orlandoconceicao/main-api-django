from software_sales.courses.models import Compra, CompraStatus


def criar_compra(*, usuario, curso):
    compra = Compra.objects.create(
        usuario=usuario,
        curso=curso,
        preco=curso.preco,
        status=CompraStatus.COMPLETED
    )

    curso.total_vendas += 1
    curso.save(update_fields=["total_vendas"])

    return compra


def solicitar_reembolso(*, compra):
    compra.status = CompraStatus.PENDING_REFUND
    compra.save(update_fields=["status"])

    return compra


def aprovar_reembolso(*, compra):
    compra.status = CompraStatus.REFUNDED
    compra.save(update_fields=["status"])

    return compra


def recusar_reembolso(*, compra):
    compra.status = CompraStatus.COMPLETED
    compra.save(update_fields=["status"])

    return compra