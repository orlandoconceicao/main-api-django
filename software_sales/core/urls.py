from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# HOME DA API
def api_home(request):
    return JsonResponse({
        "message": "API backend online",
        "version": "v1",
        "status": "online",
        "environment": "development",
        "mode": "demo",

        "architecture": {
            "api": "Django REST Framework",
            "auth": "JWT via Simple JWT",
            "database": "PostgreSQL / SQLite",
            "deployment": "Docker + Celery + Redis",
            "design": "Services, selectors, audit logging",
        },

        "docs": {
            "swagger": "/swagger/",
            "redoc": "/redoc/"
        },

        "auth": {
            "token": "/api/token/",
            "refresh": "/api/token/refresh/",
            "note": "Use credenciais de usuário existentes para autenticação.",
            "swagger_authorize": "No Swagger, clique em Authorize e use: Bearer <seu_token>"
        },

        "flow": [
            "Cadastro → Login → Cursos → Compra → Histórico"
        ],

        "filters": [
            "page", "page_size", "search", "ordering", "preco__gte", "preco__lte"
        ]
    })


class TokenObtainPairViewWithDocs(TokenObtainPairView):
    @swagger_auto_schema(
        operation_summary="Login JWT",
        operation_description=(
            "Autentica o usuário e retorna os tokens JWT access/refresh. "
            "Use o token access no cabeçalho Authorization: Bearer <token>."
        ),
        tags=["Auth"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, example="orlando"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, example="Admin@123"),
            },
            required=["username", "password"],
        ),
        responses={
            200: openapi.Response(
                description="Tokens JWT retornados com sucesso",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access": openapi.Schema(type=openapi.TYPE_STRING, example="jwt_token"),
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING, example="refresh_token"),
                    },
                ),
            ),
            401: openapi.Response(
                description="Credenciais inválidas",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(type=openapi.TYPE_STRING, example="No active account found with the given credentials"),
                    },
                ),
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshViewWithDocs(TokenRefreshView):
    @swagger_auto_schema(
        operation_summary="Atualizar Token JWT",
        operation_description=(
            "Renova o token de acesso usando um refresh token válido. "
            "Use o refresh token retornado pelo endpoint de login."
        ),
        tags=["Auth"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING, example="refresh_token"),
            },
            required=["refresh"],
        ),
        responses={
            200: openapi.Response(
                description="Novo access token gerado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access": openapi.Schema(type=openapi.TYPE_STRING, example="jwt_token"),
                    },
                ),
            ),
            401: openapi.Response(
                description="Refresh token inválido ou expirado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Token is invalid or expired"),
                    },
                ),
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# SWAGGER CONFIG
schema_view = get_schema_view(
    openapi.Info(
        title="Software Sales API",
        default_version='v1',
        description=(
            "API backend para gestão de cursos, avaliações, compras e auditoria. "
            "Fornece autenticação JWT, gestão de recursos e operações transacionais no domínio educacional."
            "\n\n"
            "Principais funcionalidades:\n"
            "- Autenticação JWT e refresh de tokens\n"
            "- CRUD de cursos com informações de autor e métricas\n"
            "- Registro de avaliações de usuários\n"
            "- Gestão de compras e histórico de transações\n"
            "- Auditoria de ações administrativas\n"
            "\n"
            "Fluxo geral: cadastro de usuário → login → listagem de cursos → compra → avaliação → histórico."
        ),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


# URLS
urlpatterns = [
    path('', api_home),

    path('admin/', admin.site.urls),

    path('api/', include('software_sales.courses.urls')),

    path('api/token/', TokenObtainPairViewWithDocs.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshViewWithDocs.as_view(), name='token_refresh'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]