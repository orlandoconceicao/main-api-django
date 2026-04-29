from django.contrib import admin
from .models import Curso, Avaliacao, Compra, Usuario


# INLINES
class AvaliacaoInline(admin.TabularInline):
    model = Avaliacao
    extra = 0
    readonly_fields = ("usuario", "nota", "comentario", "criacao", "atualizacao")
    can_delete = False


class CompraInline(admin.TabularInline):
    model = Compra
    extra = 0
    readonly_fields = ("usuario", "curso", "preco", "status", "criacao", "atualizacao")
    can_delete = False


class CursoInline(admin.TabularInline):
    model = Curso
    extra = 0
    readonly_fields = ("nome", "preco", "ativo", "criacao", "atualizacao")
    can_delete = False


# CURSO ADMIN
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = (
        "id", "nome", "criado_por", "preco",
        "total_vendas", "media_avaliacoes",
        "ativo", "criacao"
    )

    list_filter = ("ativo",)
    search_fields = ("nome", "descricao", "criado_por__email")
    ordering = ("-criacao",)

    readonly_fields = (
        "total_vendas",
        "media_avaliacoes",
        "criacao",
        "atualizacao",
    )

    inlines = [AvaliacaoInline]


# AVALIACAO ADMIN
@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = (
        "id", "usuario", "curso",
        "nota", "ativo", "criacao"
    )

    list_filter = ("nota", "ativo")
    search_fields = ("usuario__email", "curso__nome", "comentario")
    ordering = ("-criacao",)

    readonly_fields = ("criacao", "atualizacao")


# COMPRA ADMIN
@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = (
        "id", "usuario", "curso",
        "preco", "status", "ativo", "criacao"
    )

    list_filter = ("status", "ativo")
    search_fields = ("usuario__email", "curso__nome")
    ordering = ("-criacao",)

    readonly_fields = ("criacao", "atualizacao")


# USUARIO ADMIN
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "id", "username", "email",
        "is_staff", "is_active"
    )

    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("id",)

    readonly_fields = ("id",)

    inlines = [CursoInline, CompraInline]