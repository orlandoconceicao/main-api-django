from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Curso, Avaliacao, Compra, Auditoria


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("id",)

    fieldsets = UserAdmin.fieldsets + (
        ("Extras", {"fields": ()}),
    )


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "preco", "total_vendas", "media_avaliacoes", "ativo")
    search_fields = ("nome",)
    list_filter = ("ativo",)


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "curso", "nota", "criacao")
    search_fields = ("usuario__username", "curso__nome")


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "curso", "preco", "status", "criacao")
    list_filter = ("status",)


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "acao", "modelo", "objeto_id", "criado_em")
    list_filter = ("acao",)