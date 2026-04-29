from django.contrib import admin
from django.urls import path, include
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
        "admin": "/admin/",
        "api": "/api/"
    })


urlpatterns = [
    path("", home),

    # Django admin
    path("admin/", admin.site.urls),

    # APIs
    path("api/", include(public_router.urls)),
    path("api/admin/", include(admin_router.urls)),

    # Docs
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
]