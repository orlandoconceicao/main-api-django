from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet,
    CursoViewSet,
    AvaliacaoViewSet,
    CompraViewSet
)

router = DefaultRouter()

router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'cursos', CursoViewSet, basename='cursos')
router.register(r'avaliacoes', AvaliacaoViewSet, basename='avaliacoes')
router.register(r'compras', CompraViewSet, basename='compras')

urlpatterns = router.urls