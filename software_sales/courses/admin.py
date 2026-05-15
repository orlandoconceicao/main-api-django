from django.contrib import admin
from .models import Usuario, Curso, Avaliacao, Compra, Auditoria


# USER
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")


# CURSO
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

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("criado_por")

    def criado_por_safe(self, obj):
        if not obj.criado_por:
            return "—"
        return obj.criado_por.username

    criado_por_safe.short_description = "Criado por"

    def total_vendas_safe(self, obj):
        return getattr(obj, "total_vendas", 0)

    total_vendas_safe.short_description = "Total vendas"

    def media_avaliacoes_safe(self, obj):
        return getattr(obj, "media_avaliacoes", 0)

    media_avaliacoes_safe.short_description = "Média avaliações"


# AVALIACAO
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
    list_filter = ("ativo",)


# COMPRA
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

    search_fields = ("usuario__username", "curso__nome")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("usuario", "curso")


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

    list_filter = ("acao",)