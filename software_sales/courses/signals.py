from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
import threading

from django.db import models
from django.db.models import F, Avg
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.db import connection

from .models import Compra, Avaliacao, Curso, CompraStatus, Auditoria

_thread_locals = threading.local()


def get_current_user():
    return getattr(_thread_locals, "user", None)


def serialize_value(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if hasattr(value, "pk"):
        return value.pk
    return value


def model_to_dict(instance):
    return {
        field.name: serialize_value(getattr(instance, field.name))
        for field in instance._meta.fields
    }


def table_exists(table_name: str) -> bool:
    try:
        return table_name in connection.introspection.table_names()
    except Exception:
        return False


def is_valid_model(sender):
    if sender._meta.app_label in ["contenttypes", "sessions", "admin"]:
        return False

    if sender.__name__ == "Auditoria":
        return False

    return True
    
# COMPRA

@receiver(pre_save, sender=Compra)
def guardar_status_anterior(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._status_anterior = sender.objects.get(pk=instance.pk).status
        except sender.DoesNotExist:
            instance._status_anterior = None
    else:
        instance._status_anterior = None


@receiver(post_save, sender=Compra)
def compra_post_save(sender, instance, created, **kwargs):
    status_anterior = getattr(instance, "_status_anterior", None)

    if instance.status == CompraStatus.COMPLETED and status_anterior != CompraStatus.COMPLETED:
        Curso.objects.filter(pk=instance.curso.pk).update(
            total_vendas=F("total_vendas") + 1
        )

    if instance.status == CompraStatus.REFUNDED and status_anterior == CompraStatus.COMPLETED:
        Curso.objects.filter(pk=instance.curso.pk).update(
            total_vendas=F("total_vendas") - 1
        )
        
# AVALIAÇÃO

@receiver([post_save, post_delete], sender=Avaliacao)
def atualizar_media(sender, instance, **kwargs):
    media = instance.curso.avaliacoes.aggregate(
        media=Avg("nota")
    )["media"] or Decimal("0.00")

    instance.curso.media_avaliacoes = Decimal(media).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    instance.curso.save(update_fields=["media_avaliacoes"])
    
# AUDITORIA

@receiver(pre_save)
def auditoria_pre_save(sender, instance, **kwargs):
    if not is_valid_model(sender):
        return

    if not instance.pk:
        return

    try:
        old = sender.objects.get(pk=instance.pk)
        instance._old_data = model_to_dict(old)
    except sender.DoesNotExist:
        instance._old_data = None


@receiver(post_save)
def auditoria_post_save(sender, instance, created, **kwargs):
    if not is_valid_model(sender):
        return

    # CRÍTICO: evita rodar antes das migrations existirem
    if not table_exists("courses_auditoria"):
        return

    try:
        old_data = getattr(instance, "_old_data", None)
        new_data = model_to_dict(instance)

        if not created and old_data == new_data:
            return

        Auditoria.objects.create(
            usuario=get_current_user(),
            acao="CREATE" if created else "UPDATE",
            modelo=sender.__name__,
            objeto_id=instance.pk,
            dados_antes=None if created else old_data,
            dados_depois=new_data
        )

    except Exception:
        return


@receiver(post_delete)
def auditoria_delete(sender, instance, **kwargs):
    if not is_valid_model(sender):
        return

    if not table_exists("courses_auditoria"):
        return

    try:
        Auditoria.objects.create(
            usuario=get_current_user(),
            acao="DELETE",
            modelo=sender.__name__,
            objeto_id=instance.pk,
            dados_antes=model_to_dict(instance),
            dados_depois=None
        )
    except Exception:
        return