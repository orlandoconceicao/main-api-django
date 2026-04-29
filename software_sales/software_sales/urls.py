from django.urls import path, include
from django.contrib import admin
from django.http import JsonResponse

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from courses.urls import public_router, admin_router


# Swagger / OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="Software Sales API",
        default_version="v1",
        description="API documentação",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# Home da API
def home(request):
    return JsonResponse({
        "status": "API rodando",
        "swagger": "/swagger/",
        "redoc": "/redoc/",
        "api": "/api/",
        "admin": "/admin/"
    })


urlpatterns = [
    # Home
    path("", home),

    # Django Admin
    path("admin/", admin.site.urls),

    # APIs públicas
    path("api/", include(public_router.urls)),

    # APIs administrativas
    path("api/admin/", include(admin_router.urls)),

    # Schema JSON (importante para Swagger e Redoc)
    path(
        "swagger.json",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json"
    ),

    # Swagger UI
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-ui"
    ),

    # ReDoc UI
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="redoc"
    ),
]