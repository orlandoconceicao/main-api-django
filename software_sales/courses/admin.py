from django.contrib import admin
from .models import Curso, Avaliacao, Compra, Usuario


# AVALIACAO INLINE
class AvaliacaoInline(admin.TabularInline):
    model = Avaliacao
    extra = 0
    readonly_fields = ("usuario", "nota", "comentario", "criacao", "atualizacao")
    can_delete = False


# COMPRA INLINE
class CompraInline(admin.TabularInline):
    model = Compra
    extra = 0

    readonly_fields = (
        "usuario",
        "preco",
        "status",
        "criacao",
        "atualizacao"
    )

    can_delete = False


# CURSO
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

    inlines = [AvaliacaoInline, CompraInline]


# AVALIACAO
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


# COMPRA
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


# USUARIO
from django.contrib.auth.admin import UserAdmin

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

    fieldsets = UserAdmin.fieldsets + (
        ("Informações extras", {
            "fields": ()
        }),
    )