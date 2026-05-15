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
        "criado_por_safe",
        "total_vendas_safe",
        "media_avaliacoes_safe",
        "ativo",
    )

    search_fields = ("nome",)
    list_filter = ("ativo",)

    # Proteção contra crash no admin
    def criado_por_safe(self, obj):
        return getattr(obj.criado_por, "username", None) or "—"

    criado_por_safe.short_description = "Criado por"

    def total_vendas_safe(self, obj):
        try:
            return obj.total_vendas
        except Exception:
            return 0

    total_vendas_safe.short_description = "Total vendas"

    def media_avaliacoes_safe(self, obj):
        try:
            return obj.media_avaliacoes
        except Exception:
            return 0

    media_avaliacoes_safe.short_description = "Média avaliações"


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