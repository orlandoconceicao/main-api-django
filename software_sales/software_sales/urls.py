from django.urls import path, include
from django.contrib import admin
from django.http import JsonResponse

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from courses.urls import public_router, admin_router


schema_view = get_schema_view(
    openapi.Info(
        title="Software Sales API",
        default_version="v1",
        description="API documentação",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def home(request):
    return JsonResponse({
        "status": "API rodando",
        "swagger": "/swagger/",
        "redoc": "/redoc/",
    })


urlpatterns = [
    path("", home),

    path("admin/", admin.site.urls),

    path("api/", include(public_router.urls)),
    path("api/admin/", include(admin_router.urls)),

    # IMPORTANTE: schema JSON separado
    path(
        "swagger.json",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json"
    ),

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