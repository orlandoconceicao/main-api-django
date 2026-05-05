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
            "test_user": {
                "username": "admin",
                "password": "Admin@123"
            }
        },

        "usage": {
            "step_1": "POST /api/token/ com username e password",
            "step_2": "copie o access token",
            "step_3": "clique em Authorize no Swagger",
            "step_4": "use: Bearer SEU_TOKEN"
        }
    })


schema_view = get_schema_view(
    openapi.Info(
        title="Software Sales API",
        default_version='v1',
        description="API de vendas de cursos com autenticação JWT",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('', api_home),

    path('admin/', admin.site.urls),

    # API
    path('api/', include('software_sales.courses.urls')),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]