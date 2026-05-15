from django.contrib import admin
from .models import Usuario, Curso, Avaliacao, Compra, Auditoria


# USUÁRIO
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_active")


# CURSO
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome",
        "preco",
        "criado_por_safe",
        "total_vendas",
        "media_avaliacoes",
        "ativo",
        "criacao",
    )

    search_fields = ("nome",)
    list_filter = ("ativo",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("criado_por")

    def criado_por_safe(self, obj):
        return obj.criado_por.username if obj.criado_por else "—"

    criado_por_safe.short_description = "Criado por"


# AVALIAÇÃO
@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "curso",
        "nota",
        "comentario",
        "ativo",
        "criacao",
    )

    search_fields = ("usuario__username", "curso__nome")
    list_filter = ("ativo", "nota")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("usuario", "curso")


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
        "criacao",
    )

    search_fields = ("usuario__username", "curso__nome")
    list_filter = ("status", "ativo")

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

    search_fields = ("modelo", "acao")
    list_filter = ("acao", "modelo")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("usuario")