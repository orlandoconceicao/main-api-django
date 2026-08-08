import threading
from contextlib import contextmanager
from datetime import date, datetime
from decimal import Decimal

from django.db import connection
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import Auditoria, Avaliacao, Compra

_thread_locals = threading.local()


def get_current_user():
    return getattr(_thread_locals, "user", None)


@contextmanager
def audit_user(user):
    previous_user = get_current_user()
    _thread_locals.user = user
    try:
        yield
    finally:
        _thread_locals.user = previous_user


def serialize_value(value):
    if isinstance(value, (date, datetime)):
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


def audit_table_exists():
    return Auditoria._meta.db_table in connection.introspection.table_names()


def is_audited_model(sender):
    return sender in {Avaliacao, Compra}


@receiver([post_save, post_delete], sender=Compra)
@receiver([post_save, post_delete], sender=Avaliacao)
def atualizar_metricas_curso(sender, instance, **kwargs):
    instance.curso.atualizar_metricas()


@receiver(pre_save)
def auditoria_pre_save(sender, instance, **kwargs):
    if not is_audited_model(sender) or not instance.pk:
        return
    try:
        instance._old_data = model_to_dict(sender.objects.get(pk=instance.pk))
    except sender.DoesNotExist:
        instance._old_data = None


@receiver(post_save)
def auditoria_post_save(sender, instance, created, **kwargs):
    if not is_audited_model(sender) or not audit_table_exists():
        return
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
        dados_depois=new_data,
    )


@receiver(post_delete)
def auditoria_delete(sender, instance, **kwargs):
    if not is_audited_model(sender) or not audit_table_exists():
        return
    Auditoria.objects.create(
        usuario=get_current_user(),
        acao="DELETE",
        modelo=sender.__name__,
        objeto_id=instance.pk,
        dados_antes=model_to_dict(instance),
    )
