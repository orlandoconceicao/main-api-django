from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Curso, Avaliacao, Compra, Auditoria


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario

    list_display = ("id", "username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("id",)

    fieldsets = UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "preco", "ativo", "total_vendas")


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "curso", "nota", "criacao")


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "curso", "preco", "status", "criacao")


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "acao", "modelo", "criado_em")