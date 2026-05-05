from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.http import JsonResponse

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# HOME DA API
def api_home(request):
    return JsonResponse({
        "message": "Software Sales API online",

        "docs": {
            "swagger": "/swagger/",
            "redoc": "/redoc/"
        },

        "auth": {
            "token": "/api/token/",
            "refresh": "/api/token/refresh/",
            "note": "Use um usuário criado no Django admin (/admin/) para autenticação"
        },

        "usage": {
            "step_1": "Acesse /admin/ e use o usuário admin do sistema",
            "step_2": "Faça login em /api/token/ com username e password",
            "step_3": "Copie o access token retornado",
            "step_4": "No Swagger clique em Authorize",
            "step_5": "Use: Bearer <seu_token>"
        }
    })


# SWAGGER CONFIG
schema_view = get_schema_view(
    openapi.Info(
        title="Software Sales API",
        default_version='v1',
        description="API de vendas de cursos com autenticação JWT",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


# URLS
urlpatterns = [
    path('', api_home),

    path('admin/', admin.site.urls),

    path('api/', include('software_sales.courses.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]