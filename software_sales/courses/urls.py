from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UsuarioViewSet,
    CursoViewSet,
    AvaliacaoViewSet,
    AdminCursoViewSet,
    AdminAvaliacaoViewSet,
    AdminCompraViewSet
)

# PUBLICO
public_router = DefaultRouter()
public_router.register(r'usuarios', UsuarioViewSet)
public_router.register(r'cursos', CursoViewSet)
public_router.register(r'avaliacoes', AvaliacaoViewSet)

# ADMIN
admin_router = DefaultRouter()
admin_router.register(r'cursos', AdminCursoViewSet)
admin_router.register(r'avaliacoes', AdminAvaliacaoViewSet)
admin_router.register(r'compras', AdminCompraViewSet)

urlpatterns = [
    path('', include(public_router.urls)),
    path('admin/', include(admin_router.urls)),
]