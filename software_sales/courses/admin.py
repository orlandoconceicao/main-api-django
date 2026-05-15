from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Usuario,
    Curso,
    Avaliacao,
    Compra,
    Auditoria
)


# USUARIO ADMIN

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario

    list_display = (
        "id",
        "username",
        "email",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
    )

    ordering = ("id",)

    fieldsets = UserAdmin.fieldsets + (
        ("Informações Extras", {
            "fields": ()
        }),
    )


# CURSO ADMIN

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome",
        "preco",
        "criado_por",
        "total_vendas",
        "media_avaliacoes",
        "ativo",
    )

    search_fields = (
        "nome",
    )

    list_filter = (
        "ativo",
        "criacao",
    )


# AVALIACAO ADMIN

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "curso",
        "nota",
        "criacao",
    )

    search_fields = (
        "usuario__username",
        "curso__nome",
    )


# COMPRA ADMIN

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "curso",
        "preco",
        "status",
        "criacao",
    )

    list_filter = (
        "status",
    )


# AUDITORIA ADMIN

@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "acao",
        "modelo",
        "objeto_id",
        "criado_em",
    )

    list_filter = (
        "acao",
        "modelo",
    )