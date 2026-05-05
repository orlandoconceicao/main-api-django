from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet,
    CursoViewSet,
    AvaliacaoViewSet,
    CompraViewSet
)

router = DefaultRouter()

# USUÁRIOS
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')

# CURSOS
router.register(r'cursos', CursoViewSet, basename='cursos')

# AVALIAÇÕES
router.register(r'avaliacoes', AvaliacaoViewSet, basename='avaliacoes')

# COMPRAS
router.register(r'compras', CompraViewSet, basename='compras')

urlpatterns = router.urls