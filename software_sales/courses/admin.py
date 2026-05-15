from django.contrib import admin
from .models import Usuario, Curso, Avaliacao, Compra, Auditoria


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")


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
    list_filter = ("ativo",)


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "curso",
        "nota",
        "comentario",
        "ativo",
    )
    search_fields = ("usuario__username", "curso__nome")


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "curso",
        "preco",
        "status",
        "ativo",
    )
    list_filter = ("status",)


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
    list_filter = ("acao",)