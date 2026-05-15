from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r"usuarios", UsuarioViewSet)
router.register(r"cursos", CursoViewSet)
router.register(r"avaliacoes", AvaliacaoViewSet)
router.register(r"compras", CompraViewSet)
router.register(r"auditoria", AuditoriaViewSet)

urlpatterns = router.urls