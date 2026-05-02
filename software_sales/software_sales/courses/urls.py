from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CompraViewSet

# ROTAS PÚBLICAS
public_router = DefaultRouter()

# por enquanto só compras (ajustado ao seu estado atual)
public_router.register(r'compras', CompraViewSet, basename='compras')

# ROTAS ADMIN (vazio por enquanto)
admin_router = DefaultRouter()

urlpatterns = [
    path('', include(public_router.urls)),
    path('api/admin/', include(admin_router.urls)),
]