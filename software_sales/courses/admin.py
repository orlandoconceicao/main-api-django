from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario

    # Colunas da listagem no admin
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )

    # Filtros laterais
    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
    )

    # Campos de busca
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    # Ordenação padrão
    ordering = ("id",)

    # Campos ao editar usuário
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informações pessoais", {"fields": ("first_name", "last_name", "email")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )

    # Campos ao criar usuário
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_staff", "is_active"),
        }),
    )