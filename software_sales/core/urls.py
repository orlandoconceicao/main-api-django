from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# SWAGGER CONFIG
schema_view = get_schema_view(
    openapi.Info(
        title="Software Sales API",
        default_version='v1',
        description="Documentação da API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# URLS
urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),


    # SUAS APIS

    path('api/courses/', include('software_sales.courses.urls')),

    # SWAGGER

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]