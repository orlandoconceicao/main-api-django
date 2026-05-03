from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet,
    CursoViewSet,
    AvaliacaoViewSet,
    CompraViewSet
)

router = DefaultRouter()

router.register(r'usuarios', UsuarioViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'avaliacoes', AvaliacaoViewSet)
router.register(r'compras', CompraViewSet)

urlpatterns = router.urls