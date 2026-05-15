from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Usuario,
    Curso,
    Avaliacao,
    Compra,
    Auditoria,
)

# USUÁRIO@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

# CURSO
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

    search_fields = ("nome",)

    list_filter = (
        "ativo",
        "criacao",
    )


# AVALIAÇÃO
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

    list_filter = ("nota",)


# COMPRA
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

    list_filter = ("status",)

    search_fields = (
        "usuario__username",
        "curso__nome",
    )


# AUDITORIA
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

    search_fields = (
        "usuario__username",
        "modelo",
    )