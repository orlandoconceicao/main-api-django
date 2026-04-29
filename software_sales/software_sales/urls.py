from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from courses.urls import public_router, admin_router


# SWAGGER
schema_view = get_schema_view(
    openapi.Info(
        title="Software Sales API",
        default_version="v1",
        description="Documentação da API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


# HOME
def home(request):
    return JsonResponse({
        "status": "API rodando",
        "docs": "/swagger/",
        "admin": "/admin/",
        "api": "/api/"
    })


# URLS
urlpatterns = [
    path("", home),

    path("admin/", admin.site.urls),

    # API
    path("api/", include(public_router.urls)),
    path("api/admin/", include(admin_router.urls)),

    # AUTH (evita erro de login se alguém tentar acessar)
    path("accounts/", include("django.contrib.auth.urls")),

    # SWAGGER
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-ui"
    ),

    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="redoc"
    ),
]